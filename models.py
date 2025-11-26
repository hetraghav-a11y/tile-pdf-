# models.py
import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "database.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Tile(Base):
    __tablename__ = "tiles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    sku = Column(String(100), nullable=True)
    size = Column(String(100), nullable=True)
    price = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(String(250), nullable=True)
    photo_path = Column(String(500), nullable=True)  # absolute path saved
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=True)
    logo_path = Column(String(500), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(120), nullable=True)

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized at", DB_PATH)
