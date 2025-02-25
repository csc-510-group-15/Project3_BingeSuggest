import unittest
import json
import sys
from pathlib import Path
import os

sys.path.append(str(Path(__file__).resolve().parents[2]))
# pylint: disable=wrong-import-position

from src.recommenderapp.app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_login_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"login", response.data)

    def test_predict_g(self):
        data = {"movie_list": ["Inception", "The Matrix"]}
        response = self.app.post(
            "/genreBased", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("recommendations", response.json)
        self.assertIn("genres", response.json)
        self.assertIn("imdb_id", response.json)


if __name__ == "__main__":
    unittest.main()
