import sys
import unittest
import warnings
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
# pylint: disable=wrong-import-position
from src.prediction_scripts.item_based import (
    recommend_for_new_user_g,
    recommend_for_new_user_all,
    recommend_for_new_user_d,
    recommend_for_new_user_a,
)
# pylint: enable=wrong-import-position

warnings.filterwarnings("ignore")


class Tests(unittest.TestCase):
    """
    Test cases for movie predictions
    """

    def test_genre_prediction(self):
        ts = [
            {"title": "The Hangover (2009)", "rating": 5.0},
        ]
        recommendations, _, _ = recommend_for_new_user_g(ts)
        self.assertTrue("Forrest Gump (1994)" in recommendations)

    def test_all_prediction(self):
        ts = [
            {"title": "Iron Man (2008)", "rating": 5.0},
            {"title": "Thor (2011)", "rating": 5.0},
            {"title": "Captain America: The First Avenger (2011)", "rating": 5.0},
        ]
        recommendations, _, _ = recommend_for_new_user_all(ts)
        self.assertTrue(
            "The Avengers (2012)" in recommendations
            and "Captain America: Civil War (2016)" in recommendations
        )

    def test_director_prediction(self):
        ts = [
            {"title": "Lincoln (2012)", "rating": 5.0},
        ]
        recommendations, _, _ = recommend_for_new_user_d(ts)
        self.assertTrue("Catch Me If You Can (2002)" in recommendations)

    def test_actor_prediction(self):
        ts = [
            {"title": "Total Recall (1990)", "rating": 5.0},
            {"title": "Predator (1987)", "rating": 5.0},
            {"title": "Pumping Iron (1977)", "rating": 5.0},
        ]
        recommendations, _, _ = recommend_for_new_user_a(ts)
        self.assertTrue("RoboCop (1987)" in recommendations)

    def test_genre_multiple_ratings(self):
        ts = [
            {"title": "The Hangover (2009)", "rating": 5.0},
            {"title": "Step Brothers (2008)", "rating": 4.5},
        ]
        recommendations, _, _ = recommend_for_new_user_g(ts)
        self.assertTrue("Forrest Gump (1994)" in recommendations)

    def test_all_multiple_ratings(self):
        ts = [
            {"title": "Iron Man (2008)", "rating": 5.0},
            {"title": "Thor (2011)", "rating": 4.0},
            {"title": "Captain America: The First Avenger (2011)", "rating": 3.5},
        ]
        recommendations, _, _ = recommend_for_new_user_all(ts)
        self.assertTrue("The Avengers (2012)" in recommendations)

    def test_director_multiple_ratings(self):
        ts = [
            {"title": "Lincoln (2012)", "rating": 5.0},
            {"title": "The Post (2017)", "rating": 4.5},
        ]
        recommendations, _, _ = recommend_for_new_user_d(ts)
        self.assertTrue("Catch Me If You Can (2002)" in recommendations)

    def test_actor_multiple_ratings(self):
        ts = [
            {"title": "Total Recall (1990)", "rating": 5.0},
            {"title": "Predator (1987)", "rating": 4.5},
            {"title": "Pumping Iron (1977)", "rating": 4.0},
        ]
        recommendations, _, _ = recommend_for_new_user_a(ts)
        self.assertTrue("RoboCop (1987)" in recommendations)


if __name__ == "__main__":
    unittest.main()
