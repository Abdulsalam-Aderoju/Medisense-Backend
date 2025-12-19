from fastapi import FastAPI
from routers import patients, inventory, auth, reports, workload
from database import Base, engine
from models import User, Inventory, RestockRequest
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "https://medisense-khaki.vercel.app"
]




# Create all tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hack Health API",
    description="API for managing patients and AI-based triage in PHC settings",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allows the origins listed above
    allow_credentials=True,
    allow_methods=["*"],         # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],         # Allows all headers
)

# Include your patient router
app.include_router(auth.router)
app.include_router(patients.router) # Here
app.include_router(inventory.router)
app.include_router(reports.router)
app.include_router(workload.router)




@app.get("/")
def root():
    return {"message": "Welcome, Build and Show The World!"}
