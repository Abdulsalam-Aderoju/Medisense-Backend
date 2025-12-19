from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime, Float, ForeignKey, Boolean, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime, date
import enum
from database import Base


# ---------- ENUM DEFINITIONS ----------
class Sex(enum.Enum):
    Male = "Male"
    Female = "Female"

class VisitType(enum.Enum):
    Emergency = "Emergency"
    Acute = "Acute"
    Routine = "Routine"
    FollowUp = "Follow-up"

SexEnum = ENUM(Sex, name="sex_enum", create_type=True)
VisitTypeEnum = ENUM(VisitType, name="visit_type_enum", create_type=True)






# ---------------- USERS ----------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)          # "phc" or "lga"

    # ← ONLY THESE THREE LINES ARE NEW
    phc_id = Column(String, nullable=True, index=True)
    phc_name = Column(String, nullable=True)
    lga_id = Column(String, nullable=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    

# ---------------- INVENTORY ----------------
class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    phc_id = Column(String, nullable=False, index=True)        # "phc-007"
    phc_name = Column(String, nullable=False)
    item_name = Column(String, nullable=False)
    item_type = Column(String, default="drug")
    current_stock = Column(Integer, default=0)
    unit = Column(String, default="units")
    daily_consumption_rate = Column(Float, default=0.0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class RestockRequest(Base):
    __tablename__ = "restock_requests"
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    quantity_needed = Column(Integer, nullable=False)
    phc_id = Column(String, nullable=False, index=True)
    phc_name = Column(String, nullable=False)
    lga_id = Column(String, nullable=False, index=True)
    requested_by = Column(String, nullable=False)          # operator_name → real person today
    request_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="pending")            # pending, approved, declined
    comments = Column(String, nullable=True)
    processed_by = Column(String, nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    priority_level = Column(String, nullable=True)




# ---------- PATIENTS ----------
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    age = Column(Integer, nullable=False)
    sex = Column(SexEnum, nullable=False)
    symptoms = Column(ARRAY(String), nullable=False)
    visit_type = Column(VisitTypeEnum, nullable=False)
    vitals = Column(Text, nullable=True)
    medical_history = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)





# In models.py - Add lga_id to these tables
class Issue(Base):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True, index=True)
    phc_id = Column(String, nullable=False, index=True)
    lga_id = Column(String, nullable=False, index=True) # <--- NEW
    phc_name = Column(String, nullable=True)           # <--- Useful for Admin UI
    category = Column(String, nullable=False)
    priority = Column(String, default="Medium")
    description = Column(String, nullable=False)
    status = Column(String, default="Open") # Open, In Progress, Resolved
    created_at = Column(DateTime, default=datetime.utcnow)

class MonthlyReport(Base):
    __tablename__ = "monthly_reports"
    id = Column(Integer, primary_key=True, index=True)
    phc_id = Column(String, nullable=False, index=True)
    lga_id = Column(String, nullable=False, index=True) # <--- NEW
    phc_name = Column(String, nullable=True)           # <--- NEW
    month = Column(String, nullable=False)
    content = Column(String, nullable=False) 
    status = Column(String, default="Draft")
    created_at = Column(DateTime, default=datetime.utcnow)



class DailyWorkload(Base):
    __tablename__ = "daily_workload"
    
    id = Column(Integer, primary_key=True, index=True)
    phc_id = Column(String, nullable=False, index=True)
    date = Column(Date, default=lambda: datetime.utcnow().date(), index=True)
    patient_count = Column(Integer, default=0)
    capacity = Column(Integer, default=50)




