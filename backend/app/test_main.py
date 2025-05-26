import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from main import app, get_db
from db.models import Base

# Create test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_pantry.db"
test_engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def test_db():
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    yield
    # Drop tables after test
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_pantry_items():
    return [
        {
            "name": "Milk",
            "quantity": 2,
            "unit": "gallons",
            "added_date": "2024-01-15T10:30:00",
            "barcode": "123456789"
        },
        {
            "name": "Bread",
            "quantity": 1,
            "unit": "loaf",
            "added_date": "2024-01-15T10:35:00",
            "barcode": "987654321"
        },
        {
            "name": "Eggs",
            "quantity": 12,
            "unit": "count",
            "added_date": "2024-01-15T10:40:00",
            "barcode": "456789123"
        },
        {
            "name": "Chicken Breast",
            "quantity": 3,
            "unit": "lbs",
            "added_date": "2024-01-15T10:45:00",
            "barcode": "789123456"
        },
        {
            "name": "Rice",
            "quantity": 5,
            "unit": "lbs",
            "added_date": "2024-01-15T10:50:00",
            "barcode": "321654987"
        }
    ]

def test_create_pantry_items(client, test_db, sample_pantry_items):
    """Test creating multiple pantry items"""
    created_items = []
    
    for item_data in sample_pantry_items:
        response = client.post("/pantry-items/", json=item_data)
        assert response.status_code == 200
        created_item = response.json()
        assert created_item["name"] == item_data["name"]
        assert created_item["quantity"] == item_data["quantity"]
        assert created_item["unit"] == item_data["unit"]
        created_items.append(created_item)
    
    assert len(created_items) == 5

def test_read_all_pantry_items(client, test_db, sample_pantry_items):
    """Test reading all pantry items"""
    # First create some items
    for item_data in sample_pantry_items:
        client.post("/pantry-items/", json=item_data)
    
    # Now read all items
    response = client.get("/pantry-items/")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 5
    assert items[0]["name"] == "Milk"

def test_read_single_pantry_item(client, test_db, sample_pantry_items):
    """Test reading a single pantry item"""
    # Create an item first
    item_data = sample_pantry_items[0]
    create_response = client.post("/pantry-items/", json=item_data)
    created_item = create_response.json()
    
    # Read the item
    response = client.get(f"/pantry-items/{created_item['id']}")
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "Milk"
    assert item["quantity"] == 2
    assert item["unit"] == "gallons"

def test_update_pantry_item(client, test_db, sample_pantry_items):
    """Test updating a pantry item"""
    # Create an item first
    item_data = sample_pantry_items[0]
    create_response = client.post("/pantry-items/", json=item_data)
    created_item = create_response.json()
    
    # Update the item
    update_data = {
        "name": "Almond Milk",
        "quantity": 1,
        "unit": "carton",
        "added_date": "2024-01-15T11:00:00",
        "barcode": "123456789"
    }
    response = client.put(f"/pantry-items/{created_item['id']}", json=update_data)
    assert response.status_code == 200
    updated_item = response.json()
    assert updated_item["name"] == "Almond Milk"
    assert updated_item["quantity"] == 1
    assert updated_item["unit"] == "carton"

def test_delete_pantry_item(client, test_db, sample_pantry_items):
    """Test deleting a pantry item"""
    # Create an item first
    item_data = sample_pantry_items[0]
    create_response = client.post("/pantry-items/", json=item_data)
    created_item = create_response.json()
    
    # Delete the item
    response = client.delete(f"/pantry-items/{created_item['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted successfully"
    
    # Verify item is deleted
    get_response = client.get(f"/pantry-items/{created_item['id']}")
    assert get_response.status_code == 404

def test_pagination(client, test_db, sample_pantry_items):
    """Test pagination with skip and limit"""
    # Create all items
    for item_data in sample_pantry_items:
        client.post("/pantry-items/", json=item_data)
    
    # Test pagination
    response = client.get("/pantry-items/?skip=2&limit=2")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2

def test_item_not_found(client, test_db):
    """Test error handling for non-existent items"""
    response = client.get("/pantry-items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_complete_crud_workflow(client, test_db):
    """Test complete CRUD workflow with one item"""
    # CREATE
    item_data = {
        "name": "Test Item",
        "quantity": 10,
        "unit": "pieces",
        "added_date": "2024-01-15T12:00:00",
        "barcode": "111222333"
    }
    create_response = client.post("/pantry-items/", json=item_data)
    assert create_response.status_code == 200
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # READ
    read_response = client.get(f"/pantry-items/{item_id}")
    assert read_response.status_code == 200
    read_item = read_response.json()
    assert read_item["name"] == "Test Item"
    
    # UPDATE
    update_data = {
        "name": "Updated Test Item",
        "quantity": 5,
        "unit": "boxes",
        "added_date": "2024-01-15T13:00:00",
        "barcode": "111222333"
    }
    update_response = client.put(f"/pantry-items/{item_id}", json=update_data)
    assert update_response.status_code == 200
    updated_item = update_response.json()
    assert updated_item["name"] == "Updated Test Item"
    assert updated_item["quantity"] == 5
    
    # DELETE
    delete_response = client.delete(f"/pantry-items/{item_id}")
    assert delete_response.status_code == 200
    
    # Verify deletion
    verify_response = client.get(f"/pantry-items/{item_id}")
    assert verify_response.status_code == 404

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Test backend is working"}

@app.get("/pantry-items/")
def get_items():
    return []

@app.post("/pantry-items/")
def add_item(item: dict):
    print(f"📦 Received: {item}")
    return {"message": "Item added", "item": item}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)