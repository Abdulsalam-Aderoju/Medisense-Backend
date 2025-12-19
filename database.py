from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/hack_health"
DATABASE_URL = "postgresql://medisense_db_8n2b_user:eouQxUfjR8XSbTWZEt4N9Eo8eNZla0kb@dpg-d52mqg6mcj7s73bs29jg-a/medisense_db_8n2b"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



