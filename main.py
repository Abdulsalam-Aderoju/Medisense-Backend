from fastapi import FastAPI
from routers import patients, inventory, phc_auth, workload_monitor, feedback
from database import Base, engine


# Create all tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hack Health API",
    description="API for managing patients and AI-based triage in PHC settings",
    version="1.0.0"
)

# Include your patient router
app.include_router(phc_auth.router)
app.include_router(patients.router)
app.include_router(inventory.router)
app.include_router(workload_monitor.router)
app.include_router(feedback.router)




@app.get("/")
def root():
    return {"message": "Not Welcome!"}
