# routers/workload_monitor.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sklearn.linear_model import LinearRegression
from datetime import datetime
import numpy as np

from database import get_db
from models import PHCWorkloadLog, PHCUser
from schemas import WorkloadLogCreate, WorkloadForecastResponse, WorkloadLogResponse
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import func

router = APIRouter(prefix="/workload", tags=["Workload Monitor"])


# 1️⃣ Log PHC workload data (every 1–2 hours)
@router.post("/log", response_model=WorkloadLogResponse)
def record_workload(payload: WorkloadLogCreate, db: Session = Depends(get_db)):
    log = PHCWorkloadLog(**payload.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


# 2️⃣ Forecast tomorrow’s patient load
@router.post("/forecast/{phc_name}", response_model=WorkloadForecastResponse)
def forecast_next_day(phc_name: str, db: Session = Depends(get_db)):
    phc = db.query(PHCUser).filter(PHCUser.phc_name == phc_name).first()
    if not phc:
        raise HTTPException(status_code=404, detail="PHC not found")

    logs = (
        db.query(PHCWorkloadLog)
        .filter(PHCWorkloadLog.phc_name == phc_name)
        .order_by(PHCWorkloadLog.date.desc())
        .limit(14)
        .all()
    )

    if len(logs) < 3:
        raise HTTPException(status_code=400, detail="Not enough data to forecast")

    X = np.arange(len(logs)).reshape(-1, 1)
    y = np.array([log.completed_visits_today for log in logs])
    model = LinearRegression().fit(X, y)
    forecast = float(model.predict([[len(logs) + 1]])[0])

    # --- Threshold logic ---
    capacity = phc.capacity
    overload_days = phc.consecutive_overload_days or 0
    message = "Normal load expected tomorrow."

    if forecast > capacity:
        overload_days += 1
        message = f"⚠️ Forecast ({forecast:.1f}) exceeds capacity ({capacity})."
    else:
        overload_days = 0

    phc.consecutive_overload_days = overload_days
    db.commit()

    return WorkloadForecastResponse(
        forecast_next_day=forecast,
        capacity=capacity,
        overload_days=overload_days,
        message=message
    )


# 3️⃣ Daily reset task (runs automatically)
def reset_daily_workload(db: Session):
    today = datetime.utcnow().date()
    db.query(PHCWorkloadLog).filter(func.date(PHCWorkloadLog.date) < today).delete()
    db.commit()
    print("✅ Daily workload logs reset completed.")


# 4️⃣ Background scheduler (runs daily)
def start_scheduler(db_session_factory):
    scheduler = BackgroundScheduler(timezone="Africa/Lagos")

    scheduler.add_job(
        lambda: reset_daily_workload(db_session_factory()),
        "cron",
        hour=0,
        minute=0,
        id="daily_reset_job",
        replace_existing=True
    )

    scheduler.start()
    print("🕒 Scheduler started for daily workload resets.")
