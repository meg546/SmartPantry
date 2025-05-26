from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

Base = declarative_base()

class PantryItem(Base):
    __tablename__ = "pantry_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)
    unit = Column(String)
    added_date = Column(String)
    barcode = Column(String, nullable=True)

class PantryItemCreate(BaseModel):
    name: str
    quantity: int
    unit: str
    added_date: str
    barcode: Optional[str] = None

class PantryItemRead(BaseModel):
    id: int
    name: str
    quantity: int
    unit: str
    added_date: str
    barcode: Optional[str] = None
    
    class Config:
        from_attributes = True