import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from db.models import PantryItem, PantryItemCreate, PantryItemRead, Base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartPantry API", 
    description="API for managing pantry items",
    debug=os.getenv("DEBUG", "False").lower() == "true"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "SmartPantry backend is up"}

@app.get("/pantry-items/", response_model=list[PantryItemRead])
def read_pantry_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(PantryItem).offset(skip).limit(limit).all()
    return items

@app.post("/pantry-items/", response_model=PantryItemRead)
def create_pantry_item(item: PantryItemCreate, db: Session = Depends(get_db)):
    print(f"Received item: {item}")
    db_item = PantryItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    print(f"Added to database: {db_item.name}")
    return db_item

@app.delete("/pantry-items/{item_id}")
def delete_pantry_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(PantryItem).filter(PantryItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=os.getenv("API_HOST", "0.0.0.0"), 
        port=int(os.getenv("API_PORT", 8000))
    )





