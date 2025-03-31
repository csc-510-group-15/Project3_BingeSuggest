import sys
import unittest
import warnings
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
# pylint: disable=wrong-import-position
from src.recommenderapp.search import Search

# pylint: enable=wrong-import-position

warnings.filterwarnings("ignore")


class Tests(unittest.TestCase):
    """
    Test cases for search feature
    """

    def test_search_action(self):
        search_word = "action"
        filter = "titleBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        self.assertIsInstance(filtered_dict, list)
        self.assertLessEqual(len(filtered_dict), 10)

    def test_search_comedy(self):
        search_word = "comedy"
        filter = "titleBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        self.assertTrue(all("comedy" in title.lower() for title in filtered_dict))

    def test_search_drama(self):
        search_word = "drama"
        filter = "titleBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        self.assertIsNotNone(filtered_dict)

    def test_search_thriller(self):
        search_word = "thriller"
        filter = "titleBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        self.assertTrue(len(filtered_dict) > 0)

    def test_search_animated(self):
        search_word = "animated"
        filter = "titleBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        self.assertTrue(isinstance(filtered_dict, list))

    def test_search_romance(self):
        search_word = "romance"
        filter = "titleBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        self.assertTrue(all(isinstance(title, str) for title in filtered_dict))

    def test_search_sci_fi(self):
        search_word = "sci-fi"
        filter = "titleBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        self.assertTrue(len(filtered_dict) <= 10)

    def test_search_horror(self):
        search_word = "horror"
        filter = "titleBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        self.assertTrue(all("horror" in title.lower() for title in filtered_dict))

    def test_search_director(self):
        search_word = "spielberg"
        filter = "dirBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        self.assertTrue(all(isinstance(title, str) for title in filtered_dict))

    def test_search_actor(self):
        search_word = "dicaprio"
        filter = "actorBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        self.assertTrue(len(filtered_dict) <= 10)


if __name__ == "__main__":
    unittest.main()
