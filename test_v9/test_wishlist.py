import os
import sys
import json
import pytest
from pathlib import Path

# Ensure the repository root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# Set dummy environment variables
os.environ["DB_USER"] = "test_user"
os.environ["DB_PASSWORD"] = "test_pass"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "3306"
os.environ["DB_NAME"] = "test_db"

from src.recommenderapp.app import app

# --- Mock Database Classes ---
class MockWishlistCursor:
    def __init__(self):
        self.results = []
        self.last_execute = None

    def execute(self, query, params=None):
        self.last_execute = (query, params)
        if "SELECT" in query:
            self.results = [{
                "name": "Test Movie", 
                "imdb_id": "tt1234567",
                "time": "2023-01-01 00:00:00"
            }]
        elif "INSERT" in query:
            return True
        elif "DELETE" in query:
            return True

    def fetchall(self):
        return self.results

    def fetchone(self):
        return self.results[0] if self.results else None

    def close(self):
        pass


class MockConnection:
    def __init__(self):
        self.cursor_instance = MockWishlistCursor()

    def cursor(self, dictionary=False):
        return self.cursor_instance

    def commit(self):
        pass

    def close(self):
        pass


@pytest.fixture(autouse=True)
def patch_mysql(monkeypatch):
    import mysql.connector
    monkeypatch.setattr(
        mysql.connector, "connect", lambda *args, **kwargs: MockConnection()
    )


# --- Test Client Fixture ---
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["user_id"] = 1  # Mock logged in user
        yield client


# --- Wishlist Test Cases ---
def test_wishlist_page_status(client):
    """Test wishlist page returns 200 status code"""
    response = client.get("/wishlist")
    assert response.status_code == 200


def test_wishlist_page_content(client):
    """Test wishlist page contains correct elements"""
    response = client.get("/wishlist")
    data = response.get_data(as_text=True)
    assert "My Wishlist" in data
    assert "Search for a Movie" in data
    assert "Add" in data


def test_add_to_wishlist_success(client):
    """Test adding movie to wishlist"""
    response = client.post(
        "/add_to_wishlist",
        json={"imdb_id": "tt1234567"},
        content_type="application/json"
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["status"] == "success"
    assert "added to wishlist" in data["message"]


def test_add_to_wishlist_duplicate(client):
    """Test adding duplicate movie to wishlist"""
    # First add
    client.post("/add_to_wishlist", json={"imdb_id": "tt1234567"})
    # Second add (duplicate)
    response = client.post(
        "/add_to_wishlist", 
        json={"imdb_id": "tt1234567"}
    )
    data = json.loads(response.get_data(as_text=True))
    assert data["status"] == "info"
    assert "already in wishlist" in data["message"]


def test_add_to_wishlist_invalid_movie(client):
    """Test adding invalid movie to wishlist"""
    response = client.post(
        "/add_to_wishlist",
        json={"imdb_id": "invalid_id"},
        content_type="application/json"
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 404
    assert data["status"] == "error"
    assert "not found" in data["message"]


def test_get_wishlist_data(client):
    """Test retrieving wishlist data"""
    response = client.get("/getWishlistData")
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]
    assert "imdb_id" in data[0]
    assert "time" in data[0]


def test_delete_wishlist_item(client):
    """Test removing item from wishlist"""
    # First add a movie
    client.post("/add_to_wishlist", json={"imdb_id": "tt1234567"})
    # Then delete it
    response = client.post(
        "/deleteWishlistData",
        data=json.dumps("tt1234567"),
        content_type="application/json"
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["status"] == "success"
    assert "deleted from wishlist" in data["message"]


def test_delete_nonexistent_wishlist_item(client):
    """Test removing non-existent item from wishlist"""
    response = client.post(
        "/deleteWishlistData",
        data=json.dumps("tt0000000"),
        content_type="application/json"
    )
    data = json.loads(response.get_data(as_text=True))
    assert data["status"] == "info"
    assert "Failed to delete" in data["message"]


def test_wishlist_unauthorized_access(client):
    """Test wishlist access without authentication"""
    with client.session_transaction() as session:
        session.clear()  # Clear session to simulate logged out user
    
    response = client.get("/wishlist")
    assert response.status_code == 302  # Should redirect to login


def test_wishlist_add_requires_auth(client):
    """Test wishlist add without authentication"""
    with client.session_transaction() as session:
        session.clear()
    
    response = client.post("/add_to_wishlist", json={"imdb_id": "tt1234567"})
    assert response.status_code == 403  # Forbidden


def test_wishlist_data_structure(client):
    """Test wishlist data structure is correct"""
    response = client.get("/getWishlistData")
    data = json.loads(response.get_data(as_text=True))
    assert all(
        key in item 
        for item in data 
        for key in ["name", "imdb_id", "time"]
    )


def test_wishlist_add_with_movie_name(client):
    """Test adding to wishlist using movie name instead of imdb_id"""
    response = client.post(
        "/add_to_wishlist",
        json={"movieName": "Test Movie"},
        content_type="application/json"
    )
    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert data["status"] == "success"


def test_wishlist_add_empty_request(client):
    """Test adding to wishlist with empty request"""
    response = client.post("/add_to_wishlist", json={})
    assert response.status_code == 400


def test_wishlist_pagination(client):
    """Test wishlist pagination (if implemented)"""
    # Add multiple items first
    for i in range(15):
        client.post("/add_to_wishlist", json={"imdb_id": f"tt000000{i}"})
    
    response = client.get("/wishlist?page=1")
    data = response.get_data(as_text=True)
    assert "Showing 1-10" in data or "Page 1" in data  # Adjust based on your pagination UI


def test_wishlist_search_functionality(client):
    """Test wishlist search functionality"""
    response = client.get("/wishlist?search=test")
    data = response.get_data(as_text=True)
    assert "Test Movie" in data


def test_wishlist_sorting(client):
    """Test wishlist sorting options"""
    response = client.get("/wishlist?sort=date")
    data = json.loads(response.get_data(as_text=True))
    dates = [item["time"] for item in data]
    assert dates == sorted(dates, reverse=True)  # Assuming default is newest first


def test_wishlist_item_count(client):
    """Test wishlist item count is accurate"""
    # Add 3 items
    for i in range(3):
        client.post("/add_to_wishlist", json={"imdb_id": f"tt000000{i}"})
    
    response = client.get("/getWishlistData")
    data = json.loads(response.get_data(as_text=True))
    assert len(data) == 3


def test_wishlist_with_guest_user(client):
    """Test wishlist behavior with guest user"""
    with client.session_transaction() as session:
        session["user_id"] = "guest"
    
    response = client.get("/wishlist")
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert "My Wishlist" in data


def test_wishlist_remove_nonexistent_item(client):
    """Test removing item not in wishlist"""
    response = client.post(
        "/deleteWishlistData",
        data=json.dumps("tt9999999"),
        content_type="application/json"
    )
    data = json.loads(response.get_data(as_text=True))
    assert data["status"] == "info"
    assert "not in wishlist" in data["message"]