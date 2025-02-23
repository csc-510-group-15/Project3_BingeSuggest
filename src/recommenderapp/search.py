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

    def starts_with(self, word):
        """
        Function to check movie by title
        """
        n = len(word)
        res = []
        word = word.lower()
        for index,row in self.df.iterrows():
            curr = row["title"].lower()
            if curr[:n] == word:
                res.append(row["title"])
        return res

    def genre_search(self, word):
        """
        Function to search movies by genre
        """
        n = len(word)
        res = []
        word = word.lower()
        for index,row in self.df.iterrows():
            curr = row["genres"].lower()
            if curr[:n] == word:
                res.append(row["title"])
        return res


    def director_search(self, word):
        """
        Function to check movie by director
        """
        n = len(word)
        res = []
        word = word.lower()
        for index,row in self.df.iterrows():
            curr = row["director"].lower()
            if curr[:n] == word:
                res.append(row["title"])
        return res

    def actor_search(self, word):
        """
        Function to check movie by actor
        """
        n = len(word)
        res = []
        word = word.lower()
        for index,row in self.df.iterrows():
            curr = row["actors"].lower()
            if curr[:n] == word:
                res.append(row["title"])
        return res

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

    def results(self, word, filter):
        """
        Function to serve the result render
        """
        if(filter == "genreBased"):
            resp = self.genre_search(word)
        elif(filter == "dirBased"):
            resp = self.director_search(word)
        elif(filter == "actorBased"):
            resp = self.actor_search(word)
        elif(filter == "titleBased"):
            resp = self.starts_with(word)
        else:
            resp = self.starts_with(word)
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
