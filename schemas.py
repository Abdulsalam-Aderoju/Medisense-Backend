from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal
import enum
from datetime import datetime


class Sex(str, enum.Enum):
    """Enumeration for patient biological sex."""
    Male = "Male"
    Female = "Female"

class VisitType(str, enum.Enum):
    """Enumeration for the immediate triage/queue category."""
    Emergency = "Emergency"
    Acute = "Acute"
    Routine = "Routine"
    FollowUp = "Follow-up"





# ---------------- AUTHENTICATION SCHEMAS ----------------
class UserSignup(BaseModel):
    name: str = Field(..., min_length=3, 
    description="PHC name or LGA name, e.g. 'Igbogbo Primary Health Centre' or 'Ikorodu LGA'")
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: Literal["phc", "lga"]
    lga_id: str = Field(..., example="lga-ikorodu")

    # Only for PHC accounts
    phc_id: str | None = Field(None, example="phc-007")


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    operator_name: str = Field(..., min_length=3,
        description="Name of the person using the account today, e.g. 'Nurse Chioma'")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class UserRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        orm_mode = True




# ---------- PATIENT SCHEMAS ----------
class PatientBase(BaseModel):
    """
    Base schema defining the shared fields for Patient creation and reading.
    Fields correspond directly to the database columns (excluding DB-managed fields).
    """
    name: str = Field(..., max_length=255, description="Patient's full name.")
    age: int = Field(..., gt=0, description="Patient's age in years.")
    sex: Sex = Field(..., description="Biological sex (Male or Female).")
    
    # Note: Pydantic handles the List[str] conversion from JSON array input,
    # which maps to ARRAY(String) in PostgreSQL/SQLAlchemy.
    symptoms: List[str] = Field(..., description="List of raw symptoms reported by the patient.")
    visit_type: VisitType = Field(..., description="Triage category/intent for the visit.")

    # Vitals is stored as a JSON string in the DB (Text), so we validate it as a string here.
    # In a more advanced setup, this could be a nested Pydantic model (e.g., VitalsModel).
    vitals: Optional[str] = Field(None, description="Vitals data, stored as a JSON string (e.g., '{\"temp\": 37.0}').")
    
    medical_history: Optional[List[str]] = Field(None, description="List of known past medical conditions.")

# --- 3. Schemas for API Operations ---

class PatientCreate(PatientBase):
    """Schema used when creating a new patient record (input validation)."""
    # Inherits all required fields from PatientBase
    pass

class PatientUpdate(BaseModel):
    """
    Schema used when updating an existing patient record.
    All fields are Optional, as an update might only change one attribute.
    """
    name: Optional[str] = Field(None, max_length=255)
    age: Optional[int] = Field(None, gt=0)
    sex: Optional[Sex] = None
    symptoms: Optional[List[str]] = None
    visit_type: Optional[VisitType] = None
    vitals: Optional[str] = None
    medical_history: Optional[List[str]] = None

class PatientRead(PatientBase):
    """
    Schema used when reading or returning patient data (output serialization).
    Includes database-managed fields like ID and timestamps.
    """
    id: int = Field(..., description="Database primary key ID.")
    created_at: datetime = Field(..., description="Timestamp of record creation.")
    updated_at: datetime = Field(..., description="Timestamp of last update.")

    class Config:
        # This is essential for compatibility with SQLAlchemy ORM objects.
        # It tells Pydantic to read data from ORM attributes instead of just dictionary keys.
        from_attributes = True

class PatientCreateResponse(BaseModel):
    id: int
    name: str
    age: int
    message: str



# ---------------- INVENTORY & RESTOCK SCHEMAS ----------------
class LowStockResponse(BaseModel):
    item_name: str
    current_stock: int
    daily_consumption_rate: float
    unit: str
    days_remaining: float

class RestockRequestCreate(BaseModel):
    item_name: str
    quantity_needed: int = Field(..., gt=0)

class RestockRequestRead(BaseModel):
    id: int
    item_name: str
    quantity_needed: int
    phc_id: str
    phc_name: str
    lga_id: str
    requested_by: str
    request_date: datetime
    status: str
    comments: Optional[str] = None
    processed_by: Optional[str] = None
    priority_level: Optional[str] = None

    class Config:
        from_attributes = True

class RestockRequestUpdate(BaseModel):
    status: Literal["approved", "declined"]
    comments: Optional[str] = None

class AutoRestockResponse(BaseModel):
    created_requests: int
    skipped_items: List[str] = []

class RestockRequestEdit(BaseModel):
    item_name: Optional[str] = None
    quantity_needed: Optional[int] = Field(None, gt=0)





# --- ISSUES ---
class IssueCreate(BaseModel):
    category: str
    priority: str
    description: str

class IssueRead(IssueCreate):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

# --- REPORTS ---
class ReportGenerate(BaseModel):
    month_str: str # "2025-10"

class ReportUpdate(BaseModel):
    content: str # User edits the AI text

class ReportRead(BaseModel):
    id: int
    month: str
    content: str
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

















# ---------- WORKLOAD MONITORING SCHEMAS ----------
class WorkloadLogCreate(BaseModel):
    phc_id: int
    current_queue_count: int
    avg_wait_time: float
    completed_visits_today: int

class WorkloadForecastResponse(BaseModel):
    forecast_next_day: float
    capacity: int
    overload_days: int
    message: str

class WorkloadLogResponse(BaseModel):
    id: int
    phc_id: int
    date: datetime
    current_queue_count: int
    avg_wait_time: float
    completed_visits_today: int

    class Config:
        orm_mode = True



class DailyWorkloadCreate(BaseModel):
    patient_count: int

class ForecastResponse(BaseModel):
    tomorrow_load: int
    status: str # "Optimal" or "Overwhelmed"
    message: str