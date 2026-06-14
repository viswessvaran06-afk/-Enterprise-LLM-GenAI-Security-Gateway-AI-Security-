import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.audit_log import Base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres123@localhost:5432/ai_gateway"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()