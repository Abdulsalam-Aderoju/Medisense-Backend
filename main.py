from fastapi import FastAPI
from routers import patients, inventory, phc_auth, workload_monitor, feedback
from database import Base, engine
from models import Inventory
from sqlalchemy.orm import Session

app = FastAPI(
    title="Hack Health API",
    description="API for managing patients and AI-based triage in PHC settings",
    version="1.0.0"
)

# Create all tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)


# --- SEED FUNCTION ---
# --- SEED FUNCTION ---
def seed_inventory():
    with Session(engine) as session:
        if session.query(Inventory).count() == 0:
            sample_data = [
                # PHC Turunku (
                Inventory(phc_name='PHC Turunku', item_name='Paracetamol', item_type='Drug', current_stock=2000, unit='tablets', daily_consumption_rate=100, days_remaining=round(2000 / 100, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Ibuprofen', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Amoxicillin', item_type='Drug', current_stock=500, unit='capsules', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Metronidazole', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Artemether-Lumefantrine', item_type='Drug', current_stock=300, unit='tablets', daily_consumption_rate=15, days_remaining=round(300 / 15, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Oral Rehydration Salts (ORS)', item_type='Drug', current_stock=500, unit='sachets', daily_consumption_rate=25, days_remaining=round(500 / 25, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Folic Acid', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=20, days_remaining=round(1000 / 20, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Ferrous Sulfate', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=20, days_remaining=round(1000 / 20, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Chlorpheniramine', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=15, days_remaining=round(500 / 15, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Zinc Sulfate', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=10, days_remaining=round(500 / 10, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Ceftriaxone', item_type='Drug', current_stock=50, unit='vials', daily_consumption_rate=5, days_remaining=round(50 / 5, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Salbutamol', item_type='Drug', current_stock=50, unit='inhalers', daily_consumption_rate=3, days_remaining=round(50 / 3, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Metformin', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Hydrochlorothiazide', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=15, days_remaining=round(500 / 15, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Vitamin A', item_type='Drug', current_stock=500, unit='capsules', daily_consumption_rate=10, days_remaining=round(500 / 10, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Disposable Syringes', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Sterile Gloves', item_type='Equipment', current_stock=500, unit='pairs', daily_consumption_rate=40, days_remaining=round(500 / 40, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Bandages', item_type='Equipment', current_stock=300, unit='units', daily_consumption_rate=20, days_remaining=round(300 / 20, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Alcohol Swabs', item_type='Equipment', current_stock=1000, unit='swabs', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Digital Thermometers', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.1, days_remaining=round(10 / 0.1, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Blood Pressure Cuffs', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.1, days_remaining=round(10 / 0.1, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Needles', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Cotton Wool', item_type='Equipment', current_stock=50, unit='rolls', daily_consumption_rate=5, days_remaining=round(50 / 5, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Povidone-Iodine', item_type='Equipment', current_stock=20, unit='bottles', daily_consumption_rate=1, days_remaining=round(20 / 1, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Malaria RDT Kits', item_type='Test Kit', current_stock=100, unit='kits', daily_consumption_rate=10, days_remaining=round(100 / 10, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Stethoscopes', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.05, days_remaining=round(10 / 0.05, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Pulse Oximeters', item_type='Equipment', current_stock=5, unit='units', daily_consumption_rate=0.05, days_remaining=round(5 / 0.05, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Weighing Scales', item_type='Equipment', current_stock=5, unit='units', daily_consumption_rate=0.05, days_remaining=round(5 / 0.05, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Tongue Depressors', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Turunku', item_name='Disposable Face Masks', item_type='Equipment', current_stock=1000, unit='units', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                # PHC Rigasa (
                Inventory(phc_name='PHC Rigasa', item_name='Paracetamol', item_type='Drug', current_stock=2000, unit='tablets', daily_consumption_rate=100, days_remaining=round(2000 / 100, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Ibuprofen', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Amoxicillin', item_type='Drug', current_stock=500, unit='capsules', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Metronidazole', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Artemether-Lumefantrine', item_type='Drug', current_stock=300, unit='tablets', daily_consumption_rate=15, days_remaining=round(300 / 15, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Oral Rehydration Salts (ORS)', item_type='Drug', current_stock=500, unit='sachets', daily_consumption_rate=25, days_remaining=round(500 / 25, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Folic Acid', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=20, days_remaining=round(1000 / 20, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Ferrous Sulfate', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=20, days_remaining=round(1000 / 20, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Chlorpheniramine', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=15, days_remaining=round(500 / 15, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Zinc Sulfate', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=10, days_remaining=round(500 / 10, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Ceftriaxone', item_type='Drug', current_stock=50, unit='vials', daily_consumption_rate=5, days_remaining=round(50 / 5, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Salbutamol', item_type='Drug', current_stock=50, unit='inhalers', daily_consumption_rate=3, days_remaining=round(50 / 3, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Metformin', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Hydrochlorothiazide', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=15, days_remaining=round(500 / 15, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Vitamin A', item_type='Drug', current_stock=500, unit='capsules', daily_consumption_rate=10, days_remaining=round(500 / 10, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Disposable Syringes', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Sterile Gloves', item_type='Equipment', current_stock=500, unit='pairs', daily_consumption_rate=40, days_remaining=round(500 / 40, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Bandages', item_type='Equipment', current_stock=300, unit='units', daily_consumption_rate=20, days_remaining=round(300 / 20, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Alcohol Swabs', item_type='Equipment', current_stock=1000, unit='swabs', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Digital Thermometers', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.1, days_remaining=round(10 / 0.1, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Blood Pressure Cuffs', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.1, days_remaining=round(10 / 0.1, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Needles', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Cotton Wool', item_type='Equipment', current_stock=50, unit='rolls', daily_consumption_rate=5, days_remaining=round(50 / 5, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Povidone-Iodine', item_type='Equipment', current_stock=20, unit='bottles', daily_consumption_rate=1, days_remaining=round(20 / 1, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Malaria RDT Kits', item_type='Test Kit', current_stock=100, unit='kits', daily_consumption_rate=10, days_remaining=round(100 / 10, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Stethoscopes', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.05, days_remaining=round(10 / 0.05, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Pulse Oximeters', item_type='Equipment', current_stock=5, unit='units', daily_consumption_rate=0.05, days_remaining=round(5 / 0.05, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Weighing Scales', item_type='Equipment', current_stock=5, unit='units', daily_consumption_rate=0.05, days_remaining=round(5 / 0.05, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Tongue Depressors', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Rigasa', item_name='Disposable Face Masks', item_type='Equipment', current_stock=1000, unit='units', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                # PHC Afaka (
                Inventory(phc_name='PHC Afaka', item_name='Paracetamol', item_type='Drug', current_stock=2000, unit='tablets', daily_consumption_rate=100, days_remaining=round(2000 / 100, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Ibuprofen', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Amoxicillin', item_type='Drug', current_stock=500, unit='capsules', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Metronidazole', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Artemether-Lumefantrine', item_type='Drug', current_stock=300, unit='tablets', daily_consumption_rate=15, days_remaining=round(300 / 15, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Oral Rehydration Salts (ORS)', item_type='Drug', current_stock=500, unit='sachets', daily_consumption_rate=25, days_remaining=round(500 / 25, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Folic Acid', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=20, days_remaining=round(1000 / 20, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Ferrous Sulfate', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=20, days_remaining=round(1000 / 20, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Chlorpheniramine', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=15, days_remaining=round(500 / 15, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Zinc Sulfate', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=10, days_remaining=round(500 / 10, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Ceftriaxone', item_type='Drug', current_stock=50, unit='vials', daily_consumption_rate=5, days_remaining=round(50 / 5, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Salbutamol', item_type='Drug', current_stock=50, unit='inhalers', daily_consumption_rate=3, days_remaining=round(50 / 3, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Metformin', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Hydrochlorothiazide', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=15, days_remaining=round(500 / 15, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Vitamin A', item_type='Drug', current_stock=500, unit='capsules', daily_consumption_rate=10, days_remaining=round(500 / 10, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Disposable Syringes', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Sterile Gloves', item_type='Equipment', current_stock=500, unit='pairs', daily_consumption_rate=40, days_remaining=round(500 / 40, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Bandages', item_type='Equipment', current_stock=300, unit='units', daily_consumption_rate=20, days_remaining=round(300 / 20, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Alcohol Swabs', item_type='Equipment', current_stock=1000, unit='swabs', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Digital Thermometers', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.1, days_remaining=round(10 / 0.1, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Blood Pressure Cuffs', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.1, days_remaining=round(10 / 0.1, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Needles', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Cotton Wool', item_type='Equipment', current_stock=50, unit='rolls', daily_consumption_rate=5, days_remaining=round(50 / 5, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Povidone-Iodine', item_type='Equipment', current_stock=20, unit='bottles', daily_consumption_rate=1, days_remaining=round(20 / 1, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Malaria RDT Kits', item_type='Test Kit', current_stock=100, unit='kits', daily_consumption_rate=10, days_remaining=round(100 / 10, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Stethoscopes', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.05, days_remaining=round(10 / 0.05, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Pulse Oximeters', item_type='Equipment', current_stock=5, unit='units', daily_consumption_rate=0.05, days_remaining=round(5 / 0.05, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Weighing Scales', item_type='Equipment', current_stock=5, unit='units', daily_consumption_rate=0.05, days_remaining=round(5 / 0.05, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Tongue Depressors', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Afaka', item_name='Disposable Face Masks', item_type='Equipment', current_stock=1000, unit='units', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                # PHC Kerawa (
                Inventory(phc_name='PHC Kerawa', item_name='Paracetamol', item_type='Drug', current_stock=2000, unit='tablets', daily_consumption_rate=100, days_remaining=round(2000 / 100, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Ibuprofen', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Amoxicillin', item_type='Drug', current_stock=500, unit='capsules', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Metronidazole', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Artemether-Lumefantrine', item_type='Drug', current_stock=300, unit='tablets', daily_consumption_rate=15, days_remaining=round(300 / 15, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Oral Rehydration Salts (ORS)', item_type='Drug', current_stock=500, unit='sachets', daily_consumption_rate=25, days_remaining=round(500 / 25, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Folic Acid', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=20, days_remaining=round(1000 / 20, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Ferrous Sulfate', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=20, days_remaining=round(1000 / 20, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Chlorpheniramine', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=15, days_remaining=round(500 / 15, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Zinc Sulfate', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=10, days_remaining=round(500 / 10, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Ceftriaxone', item_type='Drug', current_stock=50, unit='vials', daily_consumption_rate=5, days_remaining=round(50 / 5, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Salbutamol', item_type='Drug', current_stock=50, unit='inhalers', daily_consumption_rate=3, days_remaining=round(50 / 3, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Metformin', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Hydrochlorothiazide', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=15, days_remaining=round(500 / 15, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Vitamin A', item_type='Drug', current_stock=500, unit='capsules', daily_consumption_rate=10, days_remaining=round(500 / 10, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Disposable Syringes', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Sterile Gloves', item_type='Equipment', current_stock=500, unit='pairs', daily_consumption_rate=40, days_remaining=round(500 / 40, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Bandages', item_type='Equipment', current_stock=300, unit='units', daily_consumption_rate=20, days_remaining=round(300 / 20, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Alcohol Swabs', item_type='Equipment', current_stock=1000, unit='swabs', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Digital Thermometers', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.1, days_remaining=round(10 / 0.1, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Blood Pressure Cuffs', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.1, days_remaining=round(10 / 0.1, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Needles', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Cotton Wool', item_type='Equipment', current_stock=50, unit='rolls', daily_consumption_rate=5, days_remaining=round(50 / 5, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Povidone-Iodine', item_type='Equipment', current_stock=20, unit='bottles', daily_consumption_rate=1, days_remaining=round(20 / 1, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Malaria RDT Kits', item_type='Test Kit', current_stock=100, unit='kits', daily_consumption_rate=10, days_remaining=round(100 / 10, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Stethoscopes', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.05, days_remaining=round(10 / 0.05, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Pulse Oximeters', item_type='Equipment', current_stock=5, unit='units', daily_consumption_rate=0.05, days_remaining=round(5 / 0.05, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Weighing Scales', item_type='Equipment', current_stock=5, unit='units', daily_consumption_rate=0.05, days_remaining=round(5 / 0.05, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Tongue Depressors', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Kerawa', item_name='Disposable Face Masks', item_type='Equipment', current_stock=1000, unit='units', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                # PHC Sabon Birni (
                Inventory(phc_name='PHC Sabon Birni', item_name='Paracetamol', item_type='Drug', current_stock=2000, unit='tablets', daily_consumption_rate=100, days_remaining=round(2000 / 100, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Ibuprofen', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Amoxicillin', item_type='Drug', current_stock=500, unit='capsules', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Metronidazole', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Artemether-Lumefantrine', item_type='Drug', current_stock=300, unit='tablets', daily_consumption_rate=15, days_remaining=round(300 / 15, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Oral Rehydration Salts (ORS)', item_type='Drug', current_stock=500, unit='sachets', daily_consumption_rate=25, days_remaining=round(500 / 25, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Folic Acid', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=20, days_remaining=round(1000 / 20, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Ferrous Sulfate', item_type='Drug', current_stock=1000, unit='tablets', daily_consumption_rate=20, days_remaining=round(1000 / 20, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Chlorpheniramine', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=15, days_remaining=round(500 / 15, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Zinc Sulfate', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=10, days_remaining=round(500 / 10, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Ceftriaxone', item_type='Drug', current_stock=50, unit='vials', daily_consumption_rate=5, days_remaining=round(50 / 5, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Salbutamol', item_type='Drug', current_stock=50, unit='inhalers', daily_consumption_rate=3, days_remaining=round(50 / 3, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Metformin', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Hydrochlorothiazide', item_type='Drug', current_stock=500, unit='tablets', daily_consumption_rate=15, days_remaining=round(500 / 15, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Vitamin A', item_type='Drug', current_stock=500, unit='capsules', daily_consumption_rate=10, days_remaining=round(500 / 10, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Disposable Syringes', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Sterile Gloves', item_type='Equipment', current_stock=500, unit='pairs', daily_consumption_rate=40, days_remaining=round(500 / 40, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Bandages', item_type='Equipment', current_stock=300, unit='units', daily_consumption_rate=20, days_remaining=round(300 / 20, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Alcohol Swabs', item_type='Equipment', current_stock=1000, unit='swabs', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Digital Thermometers', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.1, days_remaining=round(10 / 0.1, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Blood Pressure Cuffs', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.1, days_remaining=round(10 / 0.1, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Needles', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=30, days_remaining=round(500 / 30, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Cotton Wool', item_type='Equipment', current_stock=50, unit='rolls', daily_consumption_rate=5, days_remaining=round(50 / 5, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Povidone-Iodine', item_type='Equipment', current_stock=20, unit='bottles', daily_consumption_rate=1, days_remaining=round(20 / 1, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Malaria RDT Kits', item_type='Test Kit', current_stock=100, unit='kits', daily_consumption_rate=10, days_remaining=round(100 / 10, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Stethoscopes', item_type='Equipment', current_stock=10, unit='units', daily_consumption_rate=0.05, days_remaining=round(10 / 0.05, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Pulse Oximeters', item_type='Equipment', current_stock=5, unit='units', daily_consumption_rate=0.05, days_remaining=round(5 / 0.05, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Weighing Scales', item_type='Equipment', current_stock=5, unit='units', daily_consumption_rate=0.05, days_remaining=round(5 / 0.05, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Tongue Depressors', item_type='Equipment', current_stock=500, unit='units', daily_consumption_rate=20, days_remaining=round(500 / 20, 2)),
                Inventory(phc_name='PHC Sabon Birni', item_name='Disposable Face Masks', item_type='Equipment', current_stock=1000, unit='units', daily_consumption_rate=50, days_remaining=round(1000 / 50, 2))
            ]
            session.add_all(sample_data)
            session.commit()
            print("✅ Inventory table seeded successfully!")
        else:
            print("ℹ️ Inventory table already has data.")


# Call seeding once at startup
seed_inventory()


# Call seeding once at startup
seed_inventory()





# Include your patient router
app.include_router(phc_auth.router)
app.include_router(patients.router)
app.include_router(inventory.router)
app.include_router(workload_monitor.router)
app.include_router(feedback.router)




@app.get("/")
def root():
    return {"message": "Not Welcome!"}
