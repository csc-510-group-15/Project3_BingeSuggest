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

    # In other test files we have tested that the recommendation algorithms work as expected.
    # Now, we want to test that the endpoints are outputting that recommendation in the proper format,
    # with the needed fields
    def test_predict_g(self):
        data = {"movie_list": ["Inception", "The Matrix"]}
        response = self.app.post(
            "/genreBased", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("recommendations", response.json)
        self.assertIn("genres", response.json)
        self.assertIn("imdb_id", response.json)

    def test_predict_g_invalid(self):
        data = {"movie_list": []}
        response = self.app.post(
            "/genreBased", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_predict_g_invalid_2(self):
        data = {"something_invalid": "test"}
        response = self.app.post(
            "/genreBased", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_predict_d(self):
        data = {"movie_list": ["Inception", "The Matrix"]}
        response = self.app.post(
            "/dirBased", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("recommendations", response.json)
        self.assertIn("genres", response.json)
        self.assertIn("imdb_id", response.json)

    def test_predict_d_invalid(self):
        data = {"movie_list": []}
        response = self.app.post(
            "/dirBased", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_predict_a(self):
        data = {"movie_list": ["Inception", "The Matrix"]}
        response = self.app.post(
            "/actorBased", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("recommendations", response.json)
        self.assertIn("genres", response.json)
        self.assertIn("imdb_id", response.json)

    def test_predict_a_invalid(self):
        data = {"movie_list": []}
        response = self.app.post(
            "/actorBased", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_predict_all(self):
        data = {"movie_list": ["Inception", "The Matrix"]}
        response = self.app.post(
            "/all", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("recommendations", response.json)
        self.assertIn("genres", response.json)
        self.assertIn("imdb_id", response.json)

    # Ensure that passing an empty list is impossible, and should return an error code
    def test_predict_all_invalid(self):
        data = {"movie_list": []}
        response = self.app.post(
            "/all", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_account_invalid(self):
        data = {"an_invalid_field": "test"}
        response = self.app.post(
            "/", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_guest(self):
        data = {"guest": "guest"}
        response = self.app.post(
            "/guest", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_guest_invalid(self):
        data = {"not_guest": "not_guest"}
        response = self.app.post(
            "/guest", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_guest_empty(self):
        data = {}
        response = self.app.post(
            "/guest", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    # We need to test that the movie page is rendering
    # Let's make sure that the movie page works with multiple differemt movies
    def test_render_movie(self):
        response = self.app.get("/movie/tt0376994")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"X-Men", response.data)

    def test_render_movie_2(self):
        response = self.app.get("/movie/tt1430132")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The Wolverine", response.data)

    def test_render_movie_3(self):
        response = self.app.get("/movie/tt0145487")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Spider-Man", response.data)

    # Now we can test some invalid imdb_ids
    def test_render_movie_invalid(self):
        response = self.app.get("/movie/tt")
        self.assertEqual(response.status_code, 404)

    def test_render_movie_invalid_2(self):
        response = self.app.get("/movie/")
        self.assertEqual(response.status_code, 404)

    def test_render_movie_invalid_3(self):
        response = self.app.get("/movie/1")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
