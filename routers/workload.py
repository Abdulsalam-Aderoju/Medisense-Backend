from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from database import get_db
from models import DailyWorkload, Issue
from schemas import DailyWorkloadCreate, ForecastResponse
from .auth import oauth2_scheme
from jose import jwt
from jwt_handler import SECRET_KEY, ALGORITHM


router = APIRouter(
    prefix="/workload",
    tags=["Workload & Forecast"]
)

def get_current_user_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    




@router.post("/submit", response_model=ForecastResponse)
def submit_daily_workload(
    data: DailyWorkloadCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload)
):
    """
    Allows a PHC to submit or update its daily patient workload.
    Automatically raises a staffing shortage issue if capacity
    is exceeded for 3 consecutive days and returns a simple forecast.
    """

    # Authorization check
    if payload.get("role") != "phc":
        raise HTTPException(
            status_code=403,
            detail="Only PHCs are allowed to log daily workload."
        )

    phc_id = payload["phc_id"]
    today = datetime.utcnow().date()
    phc_capacity = 50  # Can later be moved to a Facility model

    # 1. Save or update today's workload
    workload = (
        db.query(DailyWorkload)
        .filter(
            DailyWorkload.phc_id == phc_id,
            DailyWorkload.date == today
        )
        .first()
    )

    if workload:
        workload.patient_count = data.patient_count
    else:
        workload = DailyWorkload(
            phc_id=phc_id,
            date=today,
            patient_count=data.patient_count,
            capacity=phc_capacity
        )
        db.add(workload)

    db.commit()

    # 2. Check for 3-day overload streak
    recent_history = (
        db.query(DailyWorkload)
        .filter(DailyWorkload.phc_id == phc_id)
        .order_by(DailyWorkload.date.desc())
        .limit(3)
        .all()
    )

    if len(recent_history) == 3 and all(
        day.patient_count > day.capacity for day in recent_history
    ):
        existing_issue = (
            db.query(Issue)
            .filter(
                Issue.phc_id == phc_id,
                Issue.category == "Staffing Shortage",
                Issue.status == "Open"
            )
            .first()
        )

        if not existing_issue:
            new_issue = Issue(
                phc_id=phc_id,
                phc_name=payload.get("name"),
                lga_id=payload["lga_id"],
                category="Staffing Shortage",
                priority="High",
                description=(
                    "AUTOMATED ALERT: This PHC has exceeded its patient "
                    "capacity for three consecutive days. Immediate staffing "
                    "support is required."
                )
            )
            db.add(new_issue)
            db.commit()

    # 3. Generate simple next-day forecast (mean + 10% buffer)
    avg_load = sum(day.patient_count for day in recent_history) / len(recent_history)
    tomorrow_forecast = int(avg_load * 1.10)

    return ForecastResponse(
        tomorrow_load=tomorrow_forecast,
        status="Overwhelmed" if tomorrow_forecast > phc_capacity else "Optimal",
        message="Daily workload saved and forecast generated successfully."
    )


@router.get("/forecast", response_model=ForecastResponse)
def get_current_forecast(
    db: Session = Depends(get_db),
    payload: dict = Depends(get_current_user_payload)
):
    """
    Returns the most recent forecast for dashboard display
    without modifying stored data.
    """
    pass