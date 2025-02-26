"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""
import os
import pandas as pd

# from flask import jsonify, request, render_template


app_dir = os.path.dirname(os.path.abspath(__file__))
code_dir = os.path.dirname(app_dir)
project_dir = os.path.dirname(code_dir)


class Search:
    """
    Search feature for landing page
    """

    df = pd.read_csv(project_dir + "/data/movies.csv")

    def __init__(self):
        pass

    def anywhere(self, word, visited_words):
        """
        Function to check visited words
        """
        res = []
        word = word.lower()
        for x in self.df["title"]:
            if x not in visited_words:
                curr = x.lower()
                if word in curr:
                    res.append(x)
        return res

    def search(self, word, filter):
        """
        Function for searching movie data and returning results based on input
        :param word: the keyword to search, the input the user types in the box
        :param filter: the choice selected in the dropdown next to the textbox
        :return: title of film matching criteria
        """
        # n = len(word)
        res = []
        word = word.lower()
        filter_key = ""

        if filter == "genreBased":
            filter_key = "genres"
        elif filter == "dirBased":
            filter_key = "director"
        elif filter == "actorBased":
            filter_key = "actors"
        elif filter == "titleBased":
            filter_key = "title"
        else:
            filter_key = "title"

        for index, row in self.df.iterrows():
            curr = row[filter_key].lower()
            if word in curr:
                res.append(row["title"])

        return res

    def results(self, word, filter):
        """
        Function to get the results from the search
        :param word: user input from textbox
        :param filter: choice from dropdown
        :return: result list
        """

        resp = self.search(word, filter)
        visited_words = set()
        for x in resp:
            visited_words.add(x)
        anywhere = self.anywhere(word, visited_words)
        resp.extend(anywhere)
        return resp

    def results_top_ten(self, word, filter):
        """
        Function to get top 10 results
        """
        return self.results(word, filter)[:10]


# if __name__ == "__main__":
#    app.run()
