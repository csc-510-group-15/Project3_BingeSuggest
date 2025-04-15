import os
import sys
import json
from pathlib import Path
import pytest

# Ensure the repository root is in sys.path so that we can import modules from src.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


# sys.path.append(str(Path(__file__).resolve().parents[2]))
# pylint: disable=wrong-import-position

from src.recommenderapp.app import app

# --- Patch MySQL Connector to avoid real DB calls ---
class DummyCursor:
    def execute(self, *args, **kwargs):
        pass

    def fetchall(self):
        return []

    def fetchone(self):
        return None


class DummyConnection:
    def cursor(self, dictionary=False):
        return DummyCursor()

    def commit(self):
        pass

    def close(self):
        pass


@pytest.fixture(autouse=True)
def patch_mysql_connect(monkeypatch):
    import mysql.connector

    monkeypatch.setattr(
        mysql.connector, "connect", lambda *args, **kwargs: DummyConnection()
    )


# ------------------
# Pytest Client Fixture
# ------------------
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# def setUp(self):
#         self.app = app.test_client()
#         self.app.testing = True

def test_login_page(client):
    response = client.get("/")
    assert (response.status_code == 200)
    assert (b"login" in response.data)

# In other test files we have tested that the recommendation algorithms work as expected.
# Now, we want to test that the endpoints are outputting that recommendation in the proper format,
# with the needed fields
def test_predict_g(client):
    data = {"movie_list": ["Inception", "The Matrix"]}
    response = client.post(
        "/genreBased", data=json.dumps(data), content_type="application/json"
    )
    assert (response.status_code == 200)
    assert ("recommendations" in response.json)
    assert ("genres" in response.json)
    assert ("imdb_id" in response.json)

def test_predict_g_invalid(client):
    data = {"movie_list": []}
    response = client.post(
        "/genreBased", data=json.dumps(data), content_type="application/json"
    )
    assert (response.status_code == 400)

def test_predict_g_invalid_2(client):
    data = {"something_invalid": "test"}
    response = client.post(
        "/genreBased", data=json.dumps(data), content_type="application/json"
    )
    assert (response.status_code == 400)

def test_predict_d(client):
    data = {"movie_list": ["Inception", "The Matrix"]}
    response = client.post(
        "/dirBased", data=json.dumps(data), content_type="application/json"
    )
    assert (response.status_code == 200)
    assert ("recommendations" in response.json)
    assert ("genres" in response.json)
    assert ("imdb_id" in response.json)

def test_predict_d_invalid(client):
    data = {"movie_list": []}
    response = client.post(
        "/dirBased", data=json.dumps(data), content_type="application/json"
    )
    assert (response.status_code == 400)

def test_predict_a(client):
    data = {"movie_list": ["Inception", "The Matrix"]}
    response = client.post(
        "/actorBased", data=json.dumps(data), content_type="application/json"
    )
    assert (response.status_code == 200)
    assert ("recommendations" in response.json)
    assert ("genres" in response.json)
    assert ("imdb_id" in response.json)

def test_predict_a_invalid(client):
    data = {"movie_list": []}
    response = client.post(
        "/actorBased", data=json.dumps(data), content_type="application/json"
    )
    assert (response.status_code == 400)

def test_predict_all(client):
    data = {"movie_list": ["Inception", "The Matrix"]}
    response = client.post(
        "/all", data=json.dumps(data), content_type="application/json"
    )
    assert (response.status_code == 200)
    assert ("recommendations" in response.json)
    assert ("genres" in response.json)
    assert ("imdb_id" in response.json)

# Ensure that passing an empty list is impossible, and should return an error code
def test_predict_all_invalid(client):
    data = {"movie_list": []}
    response = client.post(
        "/all", data=json.dumps(data), content_type="application/json"
    )
    assert (response.status_code == 400)

def test_create_account_invalid(client):
    data = {"an_invalid_field": "test"}
    response = client.post(
        "/", data=json.dumps(data), content_type="application/json"
    )
    assert (response.status_code == 400)

def test_guest(client):
    data = {"guest": "guest"}
    response = client.post(
        "/guest", data=json.dumps(data), content_type="application/json"
    )
    assert (response.status_code == 200)

def test_guest_invalid(client):
    data = {"not_guest": "not_guest"}
    response = client.post(
        "/guest", data=json.dumps(data), content_type="application/json"
    )
    assert (response.status_code == 400)

def test_guest_empty(client):
    data = {}
    response = client.post(
        "/guest", data=json.dumps(data), content_type="application/json"
    )
    assert (response.status_code == 400)

# We need to test that the movie page is rendering
# Let's make sure that the movie page works with multiple differemt movies
def test_render_movie(client):
    response = client.get("/movie/tt0376994")
    assert (response.status_code == 200)
    assert (b"X-Men" in response.data)

def test_render_movie_2(client):
    response = client.get("/movie/tt1430132")
    assert (response.status_code == 200)
    assert (b"The Wolverine" in response.data)

def test_render_movie_3(client):
    response = client.get("/movie/tt0145487")
    assert (response.status_code == 200)
    assert (b"Spider-Man" in response.data)

# Now we can test some invalid imdb_ids
def test_render_movie_invalid(client):
    response = client.get("/movie/tt")
    assert (response.status_code == 404)

def test_render_movie_invalid_2(client):
    response = client.get("/movie/")
    assert (response.status_code == 404)

def test_render_movie_invalid_3(client):
    response = client.get("/movie/1")
    assert (response.status_code == 404)
