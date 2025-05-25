from pydantic import BaseModel

class PantryItemBase(BaseModel):
    name: str
    quantity: int

class PantryItemCreate(PantryItemBase):
    pass

class PantryItemRead(PantryItemBase):
    id: int

    class Config:
        from_attributes = True  # instead of orm_mode = True