from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import Inventory, RestockRequest, User
from schemas import (RestockRequestCreate, RestockRequestRead,
    RestockRequestUpdate, LowStockResponse, AutoRestockResponse, RestockRequestEdit
)
from .auth import oauth2_scheme
from jose import jwt
from jwt_handler import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/inventory", tags=["Inventory & Restock"])

# ---------------- GET CURRENT USER FROM JWT (NEW & CORRECT) ----------------
def get_current_user_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get("user_id"):
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload  # ← we use this directly — no DB lookup needed!
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ---------------- PHC: Get Low Stock Items ----------------
@router.get("/low-stock", response_model=List[LowStockResponse])
def get_low_stock_items(
    threshold_days: int = 5,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload)
):
    if payload["role"] != "phc":
        raise HTTPException(status_code=403, detail="Only PHCs can view their stock")

    phc_id = payload["phc_id"]
    items = db.query(Inventory).filter(Inventory.phc_id == phc_id).all()
    low_stock = []

    for item in items:
        if item.daily_consumption_rate and item.daily_consumption_rate > 0:
            days_left = item.current_stock / item.daily_consumption_rate
            if days_left <= threshold_days:
                low_stock.append(LowStockResponse(
                    item_name=item.item_name,
                    current_stock=item.current_stock,
                    daily_consumption_rate=item.daily_consumption_rate,
                    unit=item.unit,
                    days_remaining=round(days_left, 1)
                ))
    return low_stock



# ---------------- PHC: Create Restock Request ----------------
@router.post("/restock-requests", response_model=RestockRequestRead, status_code=201)
def create_restock_request(
    request: RestockRequestCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload)
):
    if payload["role"] != "phc":
        raise HTTPException(status_code=403, detail="Only PHCs can request restock")

    new_request = RestockRequest(
        item_name=request.item_name,
        quantity_needed=request.quantity_needed,
        phc_id=payload["phc_id"],                    
        phc_name=payload["name"],                   
        requested_by=payload["operator_name"],
        lga_id=payload["lga_id"],
        status="pending",
        request_date=datetime.utcnow()
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request


# ---------------- LGA: View All Requests in Their LGA ----------------
@router.get("/restock-requests", response_model=List[RestockRequestRead])
def get_restock_requests(
    status_filter: str = "all",          # pending, approved, declined, all
    phc_id: Optional[str] = None,        # new
    phc_name: Optional[str] = None,      # new
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload)
):
    role = payload["role"]

    if role == "phc":
        # PHC only sees their own requests
        query = db.query(RestockRequest).filter(RestockRequest.phc_id == payload["phc_id"])

    elif role == "lga":
        # LGA sees all requests inside their LGA
        query = db.query(RestockRequest).filter(RestockRequest.lga_id == payload["lga_id"])

        # Optional LGA filters
        if phc_id:
            query = query.filter(RestockRequest.phc_id == phc_id)

        if phc_name:
            query = query.filter(RestockRequest.phc_name.ilike(f"%{phc_name}%"))

    else:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if status_filter != "all":
        query = query.filter(RestockRequest.status == status_filter)

    return query.order_by(RestockRequest.request_date.desc()).all()



# ---------------- LGA: Approve or Decline Request ----------------
@router.put("/restock-requests/{request_id}", response_model=RestockRequestRead)
def update_restock_request(
    request_id: int,
    update: RestockRequestUpdate,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload)
):
    if payload["role"] != "lga":
        raise HTTPException(status_code=403, detail="Only LGA can approve/decline")

    req = db.query(RestockRequest).filter(RestockRequest.id == request_id).first()
    if not req or req.lga_id != payload["lga_id"]:
        raise HTTPException(status_code=404, detail="Request not found")

    req.status = update.status
    req.comments = update.comments or req.comments
    req.processed_by = payload["operator_name"]
    req.processed_at = datetime.utcnow()

    db.commit()
    db.refresh(req)
    return req



@router.post("/auto-restock-check", response_model=AutoRestockResponse)
def auto_restock_check(
    threshold_days: int = 5,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload)
):
    if payload["role"] != "phc":
        raise HTTPException(status_code=403, detail="Only PHCs can auto-generate restock checks")

    phc_id = payload["phc_id"]
    phc_name = payload["name"]
    operator_name = payload["operator_name"]
    lga_id = payload["lga_id"]

    # Fetch all inventory items for this PHC
    items = db.query(Inventory).filter(Inventory.phc_id == phc_id).all()

    created_count = 0
    skipped_items = []

    for item in items:

        # Skip if consumption rate invalid
        if not item.daily_consumption_rate or item.daily_consumption_rate <= 0:
            continue

        # Calculate days remaining
        days_remaining = item.current_stock / item.daily_consumption_rate

        # Only create request if days_remaining <= threshold_days
        if days_remaining > threshold_days:
            continue

        # Check for duplicate "pending" requests for same PHC & item
        pending_exists = (
            db.query(RestockRequest)
            .filter(
                RestockRequest.phc_id == phc_id,
                RestockRequest.item_name == item.item_name,
                RestockRequest.status == "pending",
            )
            .first()
        )

        if pending_exists:
            skipped_items.append(item.item_name)
            continue

        # Automatically calculate needed quantity:
        #   Enough stock for 14 days (configurable if you want)
        target_days = 14
        target_quantity = int((target_days * item.daily_consumption_rate) - item.current_stock)
        if target_quantity < 1:
            target_quantity = 1

        # Assign priority level
        if days_remaining <= 2:
            priority = "High"
        elif days_remaining <= 5:
            priority = "Medium"
        else:
            priority = "Low"

        # Create new restock request
        new_request = RestockRequest(
            item_name=item.item_name,
            quantity_needed=target_quantity,
            phc_id=phc_id,
            phc_name=phc_name,
            lga_id=lga_id,
            requested_by=operator_name,
            status="pending",
            request_date=datetime.utcnow(),
            priority_level=priority
        )

        db.add(new_request)
        created_count += 1

    db.commit()

    return AutoRestockResponse(
        created_requests=created_count,
        skipped_items=skipped_items
    )



# ---------------- PHC: Edit/Update a Pending Request ----------------
# Requires: from schemas import RestockRequestEdit
@router.put("/restock-requests/{request_id}/edit", response_model=RestockRequestRead)
def edit_pending_request(
    request_id: int,
    update_data: RestockRequestEdit,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload)
):
    # 1. Access Control: PHC Only
    if payload["role"] != "phc":
        raise HTTPException(status_code=403, detail="Only PHCs can edit their requests")

    # 2. Fetch the request ensuring it belongs to this PHC
    req = db.query(RestockRequest).filter(
        RestockRequest.id == request_id,
        RestockRequest.phc_id == payload["phc_id"]
    ).first()

    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    # 3. Constraint: Can only edit 'pending' requests
    if req.status != "pending":
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot edit request. Status is '{req.status}'. Only 'pending' requests can be edited."
        )

    # 4. Apply Updates
    if update_data.item_name:
        req.item_name = update_data.item_name
    if update_data.quantity_needed:
        req.quantity_needed = update_data.quantity_needed
    
    # 5. Update timestamp so the LGA knows it was recently modified
    req.request_date = datetime.utcnow() 

    db.commit()
    db.refresh(req)
    return req


# ---------------- PHC: Soft Cancel a Pending Request ----------------
@router.put("/restock-requests/{request_id}/cancel", response_model=RestockRequestRead)
def cancel_pending_request(
    request_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload)
):
    # 1. Access Control: PHC Only
    if payload["role"] != "phc":
        raise HTTPException(status_code=403, detail="Only PHCs can cancel requests")

    # 2. Fetch the request
    req = db.query(RestockRequest).filter(
        RestockRequest.id == request_id,
        RestockRequest.phc_id == payload["phc_id"]
    ).first()

    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    # 3. Constraint: Can only cancel 'pending' requests
    #    (This prevents canceling orders that the LGA has already approved/processed)
    if req.status != "pending":
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot cancel request. Status is '{req.status}'. Only 'pending' requests can be withdrawn."
        )

    # 4. Soft Cancel (Change status instead of deleting)
    #    Since your 'status' column is a String, we can safely set this to "cancelled"
    req.status = "cancelled"
    
    # Optional: Log who cancelled it in the comments
    req.comments = f"Cancelled by {payload.get('operator_name', 'user')}"

    db.commit()
    db.refresh(req)
    return req




# ---------------- PHC: Confirm Receipt of Stock (The Logic that updates count) ----------------
@router.post("/restock-requests/{request_id}/receive", response_model=RestockRequestRead)
def receive_restock_items(
    request_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload)
):
    # 1. Access Control: Only PHC can receive
    if payload["role"] != "phc":
        raise HTTPException(status_code=403, detail="Only PHCs can receive stock")

    # 2. Fetch the request
    req = db.query(RestockRequest).filter(
        RestockRequest.id == request_id, 
        RestockRequest.phc_id == payload["phc_id"]
    ).first()

    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    # 3. Validation: Can only receive items that are "approved"
    if req.status != "approved":
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot receive stock. Current status is '{req.status}', but must be 'approved'."
        )

    # 4. FIND THE INVENTORY ITEM to update
    inventory_item = db.query(Inventory).filter(
        Inventory.phc_id == payload["phc_id"],
        Inventory.item_name == req.item_name
    ).first()

    if not inventory_item:
        # Edge case: If item was deleted from inventory after request was made, create it or error out
        # Here we error out for safety
        raise HTTPException(status_code=404, detail=f"Item '{req.item_name}' not found in inventory to update.")

    # 5. THE MAGIC: Increase the stock level
    inventory_item.current_stock += req.quantity_needed
    inventory_item.last_updated = datetime.utcnow()

    # 6. Close the ticket
    req.status = "delivered"
    req.processed_at = datetime.utcnow() # Update timestamp to show when it arrived

    db.commit()
    db.refresh(req)
    
    return req