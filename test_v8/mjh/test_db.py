import sys
import unittest
import warnings
import os
import flask
from dotenv import load_dotenv
from pathlib import Path
import mysql.connector

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.recommenderapp.utils import (
    create_account,
    get_wall_posts,
)

warnings.filterwarnings("ignore")


class Tests(unittest.TestCase):
    """
    Test cases for DB
    """

    def setUp(self):
        print("\nrunning setup method")
        load_dotenv()
        db = mysql.connector.connect(user="root", password="root", host="127.0.0.1")
        executor = db.cursor()
        executor.execute("USE testDB;")
        executor.execute("SET FOREIGN_KEY_CHECKS=0;")
        executor.execute("DELETE FROM Users")
        executor.execute("DELETE FROM Ratings")
        executor.execute("DELETE FROM Friends")
        db.commit()

    def test_create_account(self):
        """
        Create an account and validate
        """
        load_dotenv()
        db = mysql.connector.connect(user="root", password="root", host="127.0.0.1")
        executor = db.cursor()
        executor.execute("USE testDB;")
        create_account(db, "testuser@test.com", "testUser", "password123")
        executor.execute("SELECT * FROM Users WHERE username='testUser'")
        db_result = executor.fetchall()
        self.assertEqual(len(db_result), 1)
        self.assertEqual(db_result[0][1], "testUser")
        self.assertEqual(db_result[0][2], "testuser@test.com")
        db.close()

    def test_get_wall_posts(self):
        """
        Get wall posts after creating an account and adding a review
        """
        load_dotenv()
        db = mysql.connector.connect(user="root", password="root", host="127.0.0.1")
        executor = db.cursor()
        executor.execute("USE testDB;")
        create_account(db, "testuser@test.com", "testUser", "password123")
        executor.execute("SELECT idUsers FROM Users WHERE username='testUser'")
        user_id = executor.fetchall()[0][0]
        executor.execute(
            "INSERT INTO Ratings(user_id, movie_id, score, review, time) VALUES (%s, %s, %s, %s, %s);",
            (user_id, 2, 5, "Amazing movie!", "2024-10-01"),
        )
        db.commit()
        app = flask.Flask(__name__)
        with app.test_request_context("/"):
            posts = get_wall_posts(db)
        self.assertEqual(posts.json[0]["score"], 5)
        self.assertEqual(posts.json[0]["review"], "Amazing movie!")
        db.close()



if __name__ == "__main__":
    unittest.main()
