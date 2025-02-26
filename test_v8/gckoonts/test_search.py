"""
Copyright (c) 2025 Gavin Koonts
This code is licensed under MIT license (see LICENSE for details)

@author: BingeSuggest

Test suit for search feature
"""

import sys
import unittest
import warnings
from pathlib import Path

import pytest


sys.path.append(str(Path(__file__).resolve().parents[2]))
# pylint: disable=wrong-import-position
from src.recommenderapp.search import Search

# pylint: enable=wrong-import-position

warnings.filterwarnings("ignore")


class Tests(unittest.TestCase):
    """
    Test cases for search feature
    """

    """Test Cases for Title Based Search"""

    def test_search_title_batman(self):
        """
        Test case 1
        """
        search_word = "Batman"
        filter = "titleBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "Batman Forever (1995)",
            "Batman (1989)",
            "Batman Returns (1992)",
            "Batman & Robin (1997)",
            "Batman: Mask of the Phantasm (1993)",
            "Batman (1966)",
            "Batman & Mr. Freeze: SubZero (1998)",
            "The Batman Superman Movie: World's Finest (1998)",
            "Batman Beyond: Return of the Joker (2000)",
            "Batman Begins (2005)",
        ]
        self.assertTrue(filtered_dict == expected_resp)

    def test_search_title_castle(self):
        """
        Test case 2
        """
        search_word = "castle"
        filter = "titleBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "Castle Freak (1995)",
            "The Castle (1997)",
            "Ice Castles (1978)",
            "Haunted Castle (2001)",
            "The Last Castle (2001)",
            "My Mother's Castle (1990)",
            "Castle in the Sky (1986)",
            "I Capture the Castle (2003)",
            "Lupin the Third: The Castle of Cagliostro (1979)",
            "Castle Keep (1969)",
        ]
        self.assertTrue(filtered_dict == expected_resp)

    def test_search_title_ocean(self):
        """
        Test case 3
        """
        search_word = "Ocean"
        filter = "titleBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "The Deep End of the Ocean (1999)",
            "Ocean's Eleven (1960)",
            "Ocean's Eleven (2001)",
            "Ocean's Twelve (2004)",
            "Ocean Waves (1993)",
            "Ocean's Thirteen (2007)",
            "Oceans (2009)",
            "Ocean Heaven (2010)",
            "711 Ocean Drive (1950)",
            "Planet Ocean (2012)",
        ]

        self.assertTrue(filtered_dict == expected_resp)

    def test_search_title_spindle(self):
        """
        Test case 4
        """
        search_word = "spindle"
        filter = "titleBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = []

        self.assertTrue(filtered_dict == expected_resp)

    def test_search_title_empty(self):
        """
        Test case 5
        """
        search_word = None
        filter = "titleBased"
        finder = Search()
        with pytest.raises(AttributeError):
            finder.results_top_ten(search_word, filter)

    """Test Cases for Genre Based Search"""

    def test_search_genre_comedy(self):
        """
        Test case 1
        """
        search_word = "Comedy"
        filter = "genreBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "Toy Story (1995)",
            "Grumpier Old Men (1995)",
            "Waiting to Exhale (1995)",
            "Father of the Bride Part II (1995)",
            "Sabrina (1995)",
            "The American President (1995)",
            "Dracula: Dead and Loving It (1995)",
            "Four Rooms (1995)",
            "Ace Ventura: When Nature Calls (1995)",
            "Money Train (1995)",
        ]

        self.assertTrue(filtered_dict == expected_resp)

    def test_search_genre_romance(self):
        """
        Test case 2
        """
        search_word = "romance"
        filter = "genreBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "Grumpier Old Men (1995)",
            "Waiting to Exhale (1995)",
            "Sabrina (1995)",
            "The American President (1995)",
            "Sense and Sensibility (1995)",
            "Leaving Las Vegas (1995)",
            "Persuasion (1995)",
            "Carrington (1995)",
            "It Takes Two (1995)",
            "Clueless (1995)",
        ]

        self.assertTrue(filtered_dict == expected_resp)

    def test_search_genre_drama(self):
        """
        Test case 3
        """
        search_word = "Drama"
        filter = "genreBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "Waiting to Exhale (1995)",
            "Heat (1995)",
            "Tom and Huck (1995)",
            "The American President (1995)",
            "Nixon (1995)",
            "Casino (1995)",
            "Sense and Sensibility (1995)",
            "Copycat (1995)",
            "Powder (1995)",
            "Leaving Las Vegas (1995)",
        ]

        self.assertTrue(filtered_dict == expected_resp)

    def test_search_genre_action(self):
        """
        Test case 4
        """
        search_word = "Action"
        filter = "genreBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "Heat (1995)",
            "Tom and Huck (1995)",
            "Sudden Death (1995)",
            "GoldenEye (1995)",
            "Cutthroat Island (1995)",
            "Money Train (1995)",
            "Assassins (1995)",
            "Dead Presidents (1995)",
            "Mortal Kombat (1995)",
            "Guardian Angel (1994)",
        ]

        self.assertTrue(filtered_dict == expected_resp)

    def test_search_genre_action_comedy(self):
        """
        Test case 5
        """
        search_word = "Action, Comedy"
        filter = "genreBased"
        finder = Search()
        filtered_dict = ""
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = []
        self.assertTrue(filtered_dict == expected_resp)

        """Test Cases for Director Based Search"""

    def test_search_director_forest_whitaker(self):
        """
        Test case 1
        """
        search_word = "Forest Whitaker"
        filter = "dirBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "Waiting to Exhale (1995)",
            "Hope Floats (1998)",
            "First Daughter (2004)",
            "Strapped (1993)",
        ]

        self.assertTrue(filtered_dict == expected_resp)

    def test_search_director_joseph_ruben(self):
        """
        Test case 2
        """
        search_word = "Joseph Ruben"
        filter = "dirBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "Money Train (1995)",
            "Return to Paradise (1998)",
            "Dreamscape (1984)",
            "True Believer (1989)",
            "The Stepfather (1987)",
            "The Good Son (1993)",
            "Sleeping with the Enemy (1991)",
            "The Forgotten (2004)",
            "The Pom Pom Girls (1976)",
            "Penthouse North (2013)",
        ]

        self.assertTrue(filtered_dict == expected_resp)

    def test_search_director_chris_noonan(self):
        """
        Test case 3
        """
        search_word = "Chris Noonan"
        filter = "dirBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = ["Babe (1995)", "Miss Potter (2006)"]

        self.assertTrue(filtered_dict == expected_resp)

    def test_search_director_richard_w_munchkin(self):
        """
        Test case 4
        """
        search_word = "Richard W. Munchkin"
        filter = "dirBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "Guardian Angel (1994)",
            "Ring of Fire II: Blood and Steel (1993)",
            "Fists of Iron (1995)",
        ]

        self.assertTrue(filtered_dict == expected_resp)

    def test_search_director_rumplestiltskin(self):
        """
        Test case 5
        """
        search_word = "Rumplestiltskin"
        filter = "dirBased"
        finder = Search()
        filtered_dict = ""
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = []
        self.assertTrue(filtered_dict == expected_resp)

        """Test Cases for Actor Based Search"""

    def test_search_actor_tom_hanks(self):
        """
        Test case 1
        """
        search_word = "Tom Hanks"
        filter = "actorBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "Toy Story (1995)",
            "Apollo 13 (1995)",
            "Forrest Gump (1994)",
            "Philadelphia (1993)",
            "Sleepless in Seattle (1993)",
            "Saving Private Ryan (1998)",
            "The 'Burbs (1989)",
            "Splash (1984)",
            "The Money Pit (1986)",
            "Nothing in Common (1986)",
        ]
        self.assertTrue(filtered_dict == expected_resp)

    def test_search_actor_emma_watson(self):
        """
        Test case 2
        """
        search_word = "Emma Watson"
        filter = "actorBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "Harry Potter and the Chamber of Secrets (2002)",
            "Harry Potter and the Goblet of Fire (2005)",
            "The Tale of Despereaux (2008)",
            "Ballet Shoes (2008)",
            "Harry Potter and the Deathly Hallows: Part 1 (2010)",
            "The Bling Ring (2013)",
            "Noah (2014)",
            "Regression (2015)",
            "Colonia (2016)",
            "The Circle (2017)",
        ]
        self.assertTrue(filtered_dict == expected_resp)

    def test_search_actor_keanu_reeves(self):
        """
        Test case 3
        """
        search_word = "Keanu Reeves"
        filter = "actorBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "Johnny Mnemonic (1995)",
            "A Walk in the Clouds (1995)",
            "Little Buddha (1993)",
            "Speed (1994)",
            "Even Cowgirls Get the Blues (1994)",
            "Feeling Minnesota (1996)",
            "Chain Reaction (1996)",
            "Dracula (1992)",
            "The Last Time I Committed Suicide (1997)",
            "My Own Private Idaho (1991)",
        ]
        self.assertTrue(filtered_dict == expected_resp)

    def test_search_actor_tyler_perry(self):
        """
        Test case 4
        """
        search_word = "Tyler Perry"
        filter = "actorBased"
        finder = Search()
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = [
            "Diary of a Mad Black Woman (2005)",
            "Madea's Family Reunion (2006)",
            "Why Did I Get Married? (2007)",
            "Madea Goes to Jail (2009)",
            "Meet the Browns (2008)",
            "I Can Do Bad All By Myself (2009)",
            "Why Did I Get Married Too? (2010)",
            "Madea's Witness Protection (2012)",
            "Alex Cross (2012)",
            "Gone Girl (2014)",
        ]
        self.assertTrue(filtered_dict == expected_resp)

    def test_search_actor_queen_elizabeth(self):
        """
        Test case 5
        """
        search_word = "Queen Elizabeth"
        filter = "actorBased"
        finder = Search()
        filtered_dict = ""
        filtered_dict = finder.results_top_ten(search_word, filter)
        expected_resp = []
        self.assertTrue(filtered_dict == expected_resp)


if __name__ == "__main__":
    unittest.main()
