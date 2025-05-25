from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class PantryItem(Base):
    __tablename__ = 'pantry_items'
    
    id = Column(Integer, primary_key=True, index = True)
    name = Column(String, index=True)
    quantity = Column(Integer, default=0)
    unit = Column(String, default='units')
    added_date = Column(DateTime, nullable=False)
    barcode = Column(String, unique=True, nullable=True)