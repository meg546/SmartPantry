from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db.models import PantryItem
from db.database import SessionLocal
from db.schemas import PantryItemCreate, PantryItemRead

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "SmartPantry backend in up"}

@app.get("/pantry-items/", response_model=list[PantryItemRead])
def read_pantry_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(PantryItem).offset(skip).limit(limit).all()
    return items

@app.post("/pantry-items/", response_model=PantryItemRead)
def create_pantry_item(item: PantryItemCreate, db: Session = Depends(get_db)):
    db_item = PantryItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/pantry-items/{item_id}", response_model=PantryItemRead)
def read_pantry_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(PantryItem).filter(PantryItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/pantry-items/{item_id}", response_model=PantryItemRead)
def update_pantry_item(item_id: int, item: PantryItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(PantryItem).filter(PantryItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/pantry-items/{item_id}")
def delete_pantry_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(PantryItem).filter(PantryItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}





