# import os
# import sys
# import warnings
# import flask
# import json

# from pathlib import Path
# import pytest

# from dotenv import load_dotenv
# import mysql.connector

# # Ensure the repository root is in sys.path so that we can import modules from src.
# sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# from src.recommenderapp.app import app

# from src.recommenderapp.utils import (
#     create_account,
#     get_wall_posts,
# )

# # --- Patch MySQL Connector to avoid real DB calls ---
# class DummyCursor:
#     def execute(self, *args, **kwargs):
#         pass

#     def fetchall(self):
#         return []

#     def fetchone(self):
#         return None


# class DummyConnection:
#     def cursor(self, dictionary=False):
#         return DummyCursor()

#     def commit(self):
#         pass

#     def close(self):
#         pass


# @pytest.fixture(autouse=True)
# def patch_mysql_connect(monkeypatch):
#     import mysql.connector

#     monkeypatch.setattr(
#         mysql.connector, "connect", lambda *args, **kwargs: DummyConnection()
#     )

# # ------------------
# # Pytest Client Fixture
# # ------------------
# @pytest.fixture
# def client():
#     app.config["TESTING"] = True
#     with app.test_client() as client:
#         yield client

# warnings.filterwarnings("ignore")

# # def setUp(self):
# #     print("\nrunning setup method")
# #     load_dotenv()
# #     db = mysql.connector.connect(user="root", password="root", host="127.0.0.1")
# #     executor = db.cursor()
# #     executor.execute("USE testDB;")
# #     executor.execute("SET FOREIGN_KEY_CHECKS=0;")
# #     executor.execute("DELETE FROM Users")
# #     executor.execute("DELETE FROM Ratings")
# #     executor.execute("DELETE FROM Friends")
# #     db.commit()

# def test_create_account(client):
#     """
#     Create an account and validate
#     """
#     load_dotenv()
#     db = mysql.connector.connect(user="root", password="root", host="127.0.0.1")
#     executor = db.cursor()
#     executor.execute("USE testDB;")
#     create_account(db, "testuser@test.com", "testUser", "password123")
#     executor.execute("SELECT * FROM Users WHERE username='testUser'")
#     db_result = executor.fetchall()
#     assert (len(db_result) == 1)
#     assert (db_result[0][1] == "testUser")
#     assert (db_result[0][2] == "testuser@test.com")
#     db.close()

# def test_get_wall_posts(client):
#     """
#     Get wall posts after creating an account and adding a review
#     """
#     load_dotenv()
#     db = mysql.connector.connect(user="root", password="root", host="127.0.0.1")
#     executor = db.cursor()
#     executor.execute("USE testDB;")
#     create_account(db, "testuser@test.com", "testUser", "password123")
#     executor.execute("SELECT idUsers FROM Users WHERE username='testUser'")
#     user_id = executor.fetchall()[0][0]
#     executor.execute(
#         "INSERT INTO Ratings(user_id, movie_id, score, review, time) VALUES (%s, %s, %s, %s, %s);",
#         (user_id, 2, 5, "Amazing movie!", "2024-10-01"),
#     )
#     db.commit()
#     app2 = flask.Flask(__name__)
#     with app2.test_request_context("/"):
#         posts = get_wall_posts(db)
#     assert (posts.json[0]["score"] == 5)
#     assert (posts.json[0]["review"] == "Amazing movie!")
#     db.close()


# # if __name__ == "__main__":
# #     unittest.main()
