import os
import sys
import json
from pathlib import Path
import pytest
import pandas as pd
import random

# Ensure the repository root is in sys.path so that we can import modules from src.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# Set a dummy NEWS_API_KEY to avoid API key errors.
# os.environ["NEWS_API_KEY"] = "dummy_key"

from src.recommenderapp.app import app  # Import the Flask app
from src.recommenderapp.app import random_movie, higher_or_lower_game_page

from src.prediction_scripts.item_based import get_random_movie, get_total_movie_count


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


def test_get_random_movie():
    result = get_random_movie()
    assert "imdbID" in result.keys()


def test_get_random_movie_seeded():
    random.seed(500)
    result1 = get_random_movie()
    random.seed(500)
    result2 = get_random_movie()
    assert "imdbID" in result1.keys()
    assert "imdbID" in result2.keys()
    assert result1 == result2


def test_get_total_movie_count():
    movies = pd.read_csv(
        os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "data",
            "movies.csv",
        )
    )
    assert len(movies) == get_total_movie_count()


def test_absurdly_high_override_id():
    resp = get_random_movie(99999999999)
    assert resp == {}


def test_off_by_one_high_override_id():
    resp = get_random_movie(get_total_movie_count())
    assert resp == {}


def test_highest_possible_override_id():
    resp = get_random_movie(get_total_movie_count() - 1)
    assert "imdbID" in resp.keys()


def test_lowest_possible_override_id():
    resp = get_random_movie(0)
    assert "imdbID" in resp.keys()


def test_force_random_id():
    resp = get_random_movie(-1)
    assert "imdbID" in resp.keys()


def test_absurdly_low_override_id():
    resp = get_random_movie(-99999999999)
    assert "imdbID" in resp.keys()


def test_get_random_movie_route():
    result = random_movie()
    assert "imdbID" in result.keys()


def test_get_random_movie_seeded_route():
    random.seed(500)
    result1 = random_movie()
    random.seed(500)
    result2 = random_movie()
    assert "imdbID" in result1.keys()
    assert "imdbID" in result2.keys()
    assert result1 == result2


def test_absurdly_high_override_id_route():
    resp = random_movie(99999999999)
    assert resp == {}


def test_off_by_one_high_override_id_route():
    resp = random_movie(get_total_movie_count())
    assert resp == {}


def test_highest_possible_override_id_route():
    resp = random_movie(get_total_movie_count() - 1)
    assert "imdbID" in resp.keys()


def test_lowest_possible_override_id_route():
    resp = random_movie(0)
    assert "imdbID" in resp.keys()


def test_force_random_id_route():
    resp = random_movie(-1)
    assert "imdbID" in resp.keys()


def test_absurdly_low_override_id_route():
    resp = random_movie(-99999999999)
    assert "imdbID" in resp.keys()


def test_nonnumeric_override_id_route():
    try:
        resp = random_movie("hello")
    except:
        assert True
        return
    assert False


def test_return_id_format():
    resp = get_random_movie()
    assert "tt" in resp["imdbID"]
    resp = random_movie()
    assert "tt" in resp["imdbID"]


def test_stress_test():
    for i in range(10):
        resp = random_movie()
        assert "imdbID" in resp.keys()
        assert len(resp["imdbID"]) > 0
