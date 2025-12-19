from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from database import get_db
from models import Issue, MonthlyReport, RestockRequest, Inventory, User
from schemas import IssueCreate, IssueRead, ReportGenerate, ReportRead, ReportUpdate
from .auth import oauth2_scheme
from jose import jwt
from jwt_handler import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/reports", tags=["Reports & Issues"])

def get_current_user_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")



# ================= reports.py =================

@router.post("/issues", response_model=IssueRead)
def create_issue(issue: IssueCreate, db: Session = Depends(get_db), payload: dict = Depends(get_current_user_payload)):
    if payload["role"] != "phc":
        raise HTTPException(status_code=403, detail="Only PHCs can report issues")
    
    new_issue = Issue(
        phc_id=payload["phc_id"],
        phc_name=payload.get("name"), # Link the PHC Name for the Admin to see
        lga_id=payload["lga_id"],    # Link to the LGA jurisdiction
        category=issue.category,
        priority=issue.priority,
        description=issue.description
    )
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    return new_issue


@router.get("/issues", response_model=List[IssueRead])
def get_issues(db: Session = Depends(get_db), payload: dict = Depends(get_current_user_payload)):
    if payload["role"] == "phc":
        return db.query(Issue).filter(Issue.phc_id == payload["phc_id"]).order_by(Issue.created_at.desc()).all()
    
    # NEW: Allow LGAs to see issues for their specific area
    elif payload["role"] == "lga":
        return db.query(Issue).filter(Issue.lga_id == payload["lga_id"]).order_by(Issue.created_at.desc()).all()
    
    return []


@router.post("/generate", response_model=ReportRead)
def generate_monthly_report(data: ReportGenerate, db: Session = Depends(get_db), payload: dict = Depends(get_current_user_payload)):
    phc_id = payload["phc_id"]
    month_str = data.month_str

    # 1. Check if report already exists
    existing = db.query(MonthlyReport).filter(
        MonthlyReport.phc_id == phc_id, 
        MonthlyReport.month == month_str
    ).first()
    
    if existing:
        return existing # Return existing draft if clicked again

    # 2. "AI" LOGIC: Gather Stats
    # Count Restock Requests
    restock_count = db.query(RestockRequest).filter(
        RestockRequest.phc_id == phc_id,
        # In real app, filter by date range of month_str
    ).count()

    # Count Issues
    issue_count = db.query(Issue).filter(Issue.phc_id == phc_id).count()
    
    # Count Low Stock Items
    low_stock = db.query(Inventory).filter(Inventory.phc_id == phc_id, Inventory.current_stock < 10).count()

    # 3. Generate "AI" Narrative
    ai_text = (
        f"**Monthly Executive Summary - {month_str}**\n\n"
        f"**Operational Overview:**\n"
        f"The facility operated at standard capacity this month. We processed {restock_count} inventory restock requests to maintain supply levels. "
        f"Currently, we have {low_stock} items flagged as low stock that require attention.\n\n"
        f"**Infrastructure & Issues:**\n"
        f"We logged {issue_count} facility issues this month. Key areas of concern include Water Supply and Power stability.\n\n"
        f"**Recommendations:**\n"
        f"We request the LGA to expedite the approval of pending drug orders to ensure continuous care."
    )

    report = MonthlyReport(
        phc_id=phc_id,
        phc_name=payload.get("name"), # Store the Name for the Admin UI
        lga_id=payload["lga_id"],    # Store LGA ID so Admin can fetch it
        month=month_str,
        content=ai_text,
        status="Draft"
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

@router.get("/", response_model=List[ReportRead])
def get_reports(db: Session = Depends(get_db), payload: dict = Depends(get_current_user_payload)):
    # PHC: See their own drafts and submissions
    if payload["role"] == "phc":
        return db.query(MonthlyReport).filter(MonthlyReport.phc_id == payload["phc_id"]).order_by(MonthlyReport.month.desc()).all()
    
    # LGA: See only SUBMITTED reports in their LGA
    elif payload["role"] == "lga":
        return db.query(MonthlyReport).filter(
            MonthlyReport.lga_id == payload["lga_id"],
            MonthlyReport.status == "Submitted"
        ).order_by(MonthlyReport.created_at.desc()).all()
        
    return []


@router.put("/{report_id}", response_model=ReportRead)
def update_report(report_id: int, update: ReportUpdate, db: Session = Depends(get_db)):
    report = db.query(MonthlyReport).filter(MonthlyReport.id == report_id).first()
    if not report or report.status == "Submitted":
        raise HTTPException(status_code=400, detail="Report not found or already submitted")
    report.content = update.content
    db.commit()
    return report

@router.post("/{report_id}/submit", response_model=ReportRead)
def submit_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(MonthlyReport).filter(MonthlyReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.status = "Submitted"
    db.commit()
    return report


@router.put("/issues/{issue_id}", response_model=IssueRead)
def update_issue_status(issue_id: int, status: str, db: Session = Depends(get_db), payload: dict = Depends(get_current_user_payload)):
    if payload["role"] != "lga":
        raise HTTPException(status_code=403, detail="Only Admins can update issue status")
    issue = db.query(Issue).filter(Issue.id == issue_id, Issue.lga_id == payload["lga_id"]).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    issue.status = status
    db.commit()
    return issue