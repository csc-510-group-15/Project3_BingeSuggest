"""
Copyright (c) 2023 Nathan Kohen, Nicholas Foster, Brandon Walia, Robert Kenney
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""
# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=import-error
import json
import sys
import os
import logging
import requests
import random
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    g,
    render_template,
    jsonify,
    session,
)
from flask_cors import CORS
import mysql.connector
import requests
from dotenv import load_dotenv, find_dotenv

sys.path.append("../../")
from src.recommenderapp.utils import (
    beautify_feedback_data,
    send_email_to_user,
    create_account,
    login_to_account,
    submit_review,
    get_wall_posts,
    get_recent_movies,
    get_username,
    add_friend,
    get_friends,
    get_recent_friend_movies,
    add_to_watchlist,
    get_imdb_id_by_name,
    add_to_watched_history,
    remove_from_watched_history_util,
    create_or_update_discussion,
    get_discussion,
    get_username_data,
    remove_from_watchlist,
)
from src.recommenderapp.search import Search
from datetime import datetime
from src.prediction_scripts.item_based import (
    recommend_for_new_user_g,
    recommend_for_new_user_d,
    recommend_for_new_user_a,
    recommend_for_new_user_all,
)

sys.path.remove("../../")


app = Flask(__name__)
app.secret_key = "secret key"

cors = CORS(app, resources={r"/*": {"origins": "*"}})
user = {1: None}
comments: []


@app.route("/")
def login_page():
    """
    Renders the login page.
    """
    return render_template("login.html")


@app.route("/profile")
def profile_page():
    """
    Renders the login page.
    """
    if user[1] is not None:
        return render_template("profile.html")
    return render_template("login.html")


@app.route("/wall")
def wall_page():
    """
    Renders the wall page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("wall.html")
    return render_template("login.html")


@app.route("/review")
def review_page():
    """
    Renders the review page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("review.html")
    return render_template("login.html")


@app.route("/landing")
def landing_page():
    """
    Renders the landing page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("landing_page.html")
    return render_template("login.html")


@app.route("/search_page")
def search_page():
    """
    Renders the search page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("search_page.html")
    return render_template("login.html")


@app.route("/genreBased", methods=["POST"])
def predict_g():
    """
    Predicts movie recommendations based on user ratings.
    """
    data = json.loads(request.data)
    if "movie_list" not in data:
        return jsonify({"error": "no movie list provided"}), 400
    data1 = data["movie_list"]
    if not data1:
        return jsonify({"error": "No movies provided"}), 400
    training_data = []
    for movie in data1:
        movie_with_rating = {"title": movie, "rating": 5.0}
        if movie_with_rating not in training_data:
            training_data.append(movie_with_rating)
    recommendations, genres, imdb_id = recommend_for_new_user_g(training_data)
    recommendations, genres, imdb_id = recommendations[:10], genres[:10], imdb_id[:10]
    resp = {"recommendations": recommendations, "genres": genres, "imdb_id": imdb_id}
    print(resp)
    return resp


@app.route("/dirBased", methods=["POST"])
def predict_d():
    """
    Predicts movie recommendations based on user ratings.
    """
    data = json.loads(request.data)
    if "movie_list" not in data:
        return jsonify({"error": "no movie list provided"}), 400
    data1 = data["movie_list"]
    if not data1:
        return jsonify({"error": "No movies provided"}), 400
    training_data = []
    for movie in data1:
        movie_with_rating = {"title": movie, "rating": 5.0}
        if movie_with_rating not in training_data:
            training_data.append(movie_with_rating)
    recommendations, genres, imdb_id = recommend_for_new_user_d(training_data)
    recommendations, genres, imdb_id = recommendations[:10], genres[:10], imdb_id[:10]
    resp = {"recommendations": recommendations, "genres": genres, "imdb_id": imdb_id}
    return resp


@app.route("/actorBased", methods=["POST"])
def predict_a():
    """
    Predicts movie recommendations based on user ratings.
    """
    data = json.loads(request.data)
    if "movie_list" not in data:
        return jsonify({"error": "no movie list provided"}), 400
    data1 = data["movie_list"]
    if not data1:
        return jsonify({"error": "No movies provided"}), 400
    training_data = []
    for movie in data1:
        movie_with_rating = {"title": movie, "rating": 5.0}
        if movie_with_rating not in training_data:
            training_data.append(movie_with_rating)
    recommendations, genres, imdb_id = recommend_for_new_user_a(training_data)
    recommendations, genres, imdb_id = recommendations[:10], genres[:10], imdb_id[:10]
    resp = {"recommendations": recommendations, "genres": genres, "imdb_id": imdb_id}
    return resp


@app.route("/all", methods=["POST"])
def predict_all():
    """
    Predicts movie recommendations based on user ratings.
    """
    data = json.loads(request.data)
    if "movie_list" not in data:
        return jsonify({"error": "no movie list provided"}), 400
    data1 = data["movie_list"]
    if not data1:
        return jsonify({"error": "No movies provided"}), 400
    training_data = []
    for movie in data1:
        movie_with_rating = {"title": movie, "rating": 5.0}
        if movie_with_rating not in training_data:
            training_data.append(movie_with_rating)
    recommendations, genres, imdb_id = recommend_for_new_user_all(training_data)
    recommendations, genres, imdb_id = recommendations[:10], genres[:10], imdb_id[:10]
    resp = {"recommendations": recommendations, "genres": genres, "imdb_id": imdb_id}
    return resp


@app.route("/search", methods=["POST"])
def search():
    """
    Handles movie search requests.
    """
    term = request.form["q"]
    filter_term = request.form["filter"]
    finder = Search()
    filtered_dict = finder.results_top_ten(term, filter_term)
    resp = jsonify(filtered_dict)
    resp.status_code = 200
    return resp


@app.route("/", methods=["POST"])
def create_acc():
    """
    Handles creating a new account.
    """
    data = json.loads(request.data)
    if not ("email" in data and "username" in data and "password" in data):
        return jsonify({"error": "No email, username, or password provided"}), 400
    try:
        create_account(g.db, data["email"], data["username"], data["password"])
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return request.data


@app.route("/out", methods=["POST"])
def signout():
    """
    Handles signing out the active user
    """
    user[1] = None
    return request.data


@app.route("/log", methods=["POST"])
def login():
    """
    Handles logging in the active user
    """
    data = json.loads(request.data)
    resp = login_to_account(g.db, data["username"], data["password"])
    if resp is None:
        return 400
    user[1] = resp
    return request.data


@app.route("/friend", methods=["POST"])
def friend():
    """
    Handles adding a new friend
    """
    data = json.loads(request.data)
    add_friend(g.db, data["username"], user[1])
    return request.data


@app.route("/guest", methods=["POST"])
def guest():
    """
    Sets the user to be a guest user
    """
    data = json.loads(request.data)
    if "guest" not in data:
        return jsonify({"error": "invalid guest request"}), 400
    user[1] = data["guest"]
    return request.data


@app.route("/review", methods=["POST"])
def review():
    """
    Handles the submission of a movie review
    """
    data = request.get_json()
    movie_name = data.get("movie")
    data["imdb_id"] = get_imdb_id_by_name(g.db, movie_name)
    submit_review(g.db, user[1], movie_name, data.get("score"), data.get("review"))
    return request.data


@app.route("/getWallData", methods=["GET"])
def wall_posts():
    """
    Gets the posts for the wall
    """
    return get_wall_posts(g.db)


@app.route("/getRecentMovies", methods=["GET"])
def recent_movies():
    """
    Gets the recent movies of the active user
    """
    return get_recent_movies(g.db, user[1])


@app.route("/getRecentFriendMovies", methods=["POST"])
def recent_friend_movies():
    """
    Gets the recent movies of a certain friend
    """
    data = json.loads(request.data)
    return get_recent_friend_movies(g.db, str(data))


@app.route("/getUserName", methods=["GET"])
def username():
    """
    Gets the username of the active user
    """
    if user[1] == "guest":
        return jsonify("guest")
    return get_username(g.db, user[1])


@app.route("/getFriends", methods=["GET"])
def get_friend():
    """
    Gets the friends of the active user
    """
    return get_friends(g.db, user[1])


@app.route("/feedback", methods=["POST"])
def feedback():
    """
    Handles user feedback submission and mails the results.
    """
    data = json.loads(request.data)
    return data


@app.route("/sendMail", methods=["POST"])
def send_mail():
    """
    Handles user feedback submission and mails the results.
    """
    data = json.loads(request.data)
    user_email = data["email"]
    send_email_to_user(user_email, beautify_feedback_data(data))
    return data


@app.route("/add_to_watchlist", methods=["POST"])
def add_movie_to_watchlist():
    """
    Adds a movie to the user's watchlist.
    """
    data = request.get_json()
    print(data)
    movie_name = data.get("movieName")
    print(movie_name)
    imdb_id = (
        get_imdb_id_by_name(g.db, movie_name) if movie_name else data.get("imdb_id")
    )
    print("Got imdb id")
    if not imdb_id:
        return jsonify({"status": "error", "message": "Movie not found"}), 404
    print("imdb id is present")

    cursor = g.db.cursor()
    cursor.execute("SELECT idMovies FROM Movies WHERE imdb_id = %s", [imdb_id])
    movie_id_result = cursor.fetchone()
    print("Selected movie.")
    if movie_id_result:
        movie_id = movie_id_result[0]
        user_id = user[1]  # Assuming 'user' holds the currently logged-in user's ID
        print("Before was added.")
        # Add to watchlist and check if it was added successfully
        was_added = add_to_watchlist(g.db, user_id, movie_id)
        print(was_added)
        if was_added:
            return (
                jsonify({"status": "success", "message": "Movie added to watchlist"}),
                200,
            )
        else:
            return (
                jsonify({"status": "info", "message": "Movie already in watchlist"}),
                200,
            )
    else:
        return jsonify({"status": "error", "message": "Movie not found"}), 404


@app.route("/watchlist", methods=["GET"])
def watchlist_page():
    """
    Renders the watchlist page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("watchlist.html")
    return render_template("login.html")


@app.route("/getWatchlistData", methods=["GET"])
def get_watchlist():
    """
    Retrieves the current user's watchlist.
    """
    user_id = user[1]  # Assuming 'user' holds the currently logged-in user's ID
    cursor = g.db.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT m.name, m.imdb_id, w.time
        FROM Watchlist w
        JOIN Movies m ON w.movie_id = m.idMovies
        WHERE w.user_id = %s
        ORDER BY w.time DESC;
        """,
        [user_id],
    )
    watchlist = cursor.fetchall()
    return jsonify(watchlist), 200


@app.route("/deleteWatchlistData", methods=["POST"])
def delete_watchlist_data():
    """
    Retrieves the current user
    """
    user_id = user[1]  # Assuming 'user' holds the currently logged-in user's ID
    imdb_id = json.loads(request.data)
    idMovies, _ = remove_from_watchlist(g.db, user_id, imdb_id)

    if idMovies:
        return (
            jsonify({"status": "success", "message": "Movie deleted from watchlist"}),
            200,
        )
    else:
        return (
            jsonify(
                {"status": "info", "message": "Failed to delete movie from watchlist"}
            ),
            200,
        )


@app.route("/get_api_key", methods=["GET"])
def get_api_key():
    """
    Provides the OMDB API key securely to the frontend.
    """
    if user[1] is not None:
        return jsonify({"apikey": os.getenv("OMDB_API_KEY")})
    return jsonify({"error": "Unauthorized"}), 403


@app.route("/get_api_key_streaming", methods=["GET"])
def get_api_key_streaming():
    """
    Provides the Streaming Services API key to the frontend
    """
    if user[1] is not None:
        return jsonify({"apikey": os.getenv("STREAMING_API_KEY")})
    return jsonify({"error": "Unauthorized"}), 403


@app.route("/add_to_watched_history", methods=["POST"])
def add_movie_to_watched_history():
    """
    Adds a movie to the user's watched history.
    """
    print("Entered add_to_watched_history function")
    data = request.get_json()
    print("Request data:", data)

    # Get IMDb ID or movie name
    imdb_id = data.get("imdb_id")
    if not imdb_id:
        movie_name = data.get("movieName")
        imdb_id = get_imdb_id_by_name(g.db, movie_name) if movie_name else None

    if not imdb_id:
        return jsonify({"status": "error", "message": "Movie not found"}), 404

    print("IMDb ID obtained:", imdb_id)
    user_id = user[1]  # Assuming 'user' holds the currently logged-in user's ID

    # Call utility function to add the movie
    was_added, message = add_to_watched_history(
        g.db, user_id, imdb_id, data.get("watched_date")
    )
    status = "success" if was_added else "info"
    return jsonify({"status": status, "message": message}), 200


@app.route("/watched_history", methods=["GET"])
def watched_history_page():
    """
    Renders the watched history page.
    """
    if user[1] is not None or user[1] == "guest":
        return render_template("watched_history.html")
    return render_template("login.html")


@app.route("/getWatchedHistoryData", methods=["GET"])
def get_watched_history():
    """
    Retrieves the current user's watched history.
    """
    user_id = user[1]  # Assuming 'user' holds the currently logged-in user's ID
    cursor = g.db.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT m.name AS movie_name, m.imdb_id, wh.watched_date
        FROM WatchedHistory wh
        JOIN Movies m ON wh.movie_id = m.idMovies
        WHERE wh.user_id = %s
        ORDER BY wh.watched_date DESC;
        """,
        [user_id],
    )
    watched_history = cursor.fetchall()
    return jsonify(watched_history), 200


@app.route("/removeFromWatchedHistory", methods=["POST"])
def remove_from_watched_history():
    """
    Removes a movie from the user's watched history.
    """
    print("Entered remove_from_watched_history function")
    data = request.get_json()
    print("Request data:", data)

    imdb_id = data.get("imdb_id")
    if not imdb_id:
        return jsonify({"status": "error", "message": "IMDb ID not provided"}), 400

    user_id = user[1]  # Assuming 'user' holds the currently logged-in user's ID

    # Call utility function to remove the movie
    was_removed, message = remove_from_watched_history_util(g.db, user_id, imdb_id)
    status = "success" if was_removed else "error"
    return jsonify({"status": status, "message": message}), 200


@app.route("/success")
def success():
    """
    Renders the success page.
    """
    return render_template("success.html")


@app.route("/movie/<id>")
def moviePage(id):
    """
    Renders the movie page with description and details and discussion forum
    """
    user_id = user[1]
    us = ""
    if user_id is None or user_id == "guest":
        us = "Anonymous"
    else:
        us = get_username_data(g.db, user_id)
    r = requests.get(
        "http://www.omdbapi.com/", params={"i": id, "apikey": os.getenv("OMDB_API_KEY")}
    )
    resp = r.json()
    if "Error" in resp:
        return jsonify({"error": "Movie not found"}), 404
    data = {"movieData": r.json(), "user": us}
    return render_template("movie.html", data=data)


@app.route("/movieDiscussion/<id>", methods=["GET"])
def getMovieDisccusion(id):
    """
    Returns the discussion store for the corresponding imdbId
    """
    return get_discussion(g.db, id)


@app.route("/movieDiscussion/<id>", methods=["POST"])
def postCommentOnMovieDisccusion(id):
    """
    Returns the discussion store for the corresponding imdbId
    """
    data = request.get_json()
    data["imdb_id"] = id
    return create_or_update_discussion(g.db, data)


@app.route("/news")
def news_feed():
    news_api_key = os.getenv("NEWS_API_KEY")
    if not news_api_key:
        return jsonify({"error": "News API key not set"}), 500

    page_size = 9  # You can adjust this value as needed
    # Get page number from request arguments; default to page 1.
    page = int(request.args.get("page", 1))

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "movie OR film",
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": news_api_key,
        "pageSize": page_size,
        "page": page,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch news"}), 500

    news_data = response.json()
    articles = news_data.get("articles", [])
    total_results = news_data.get("totalResults", 0)

    # Calculate total pages (round up)
    total_pages = (total_results + page_size - 1) // page_size

    return render_template(
        "news.html", articles=articles, current_page=page, total_pages=total_pages
    )


import html  # Add this import at the top with your other imports


@app.route("/quiz")
def quiz_page():
    """
    Fetches movie trivia questions from Open Trivia DB (Entertainment: Film) and renders the quiz page.
    """
    url = "https://opentdb.com/api.php"
    params = {"amount": 10, "category": 11, "type": "multiple"}  # Entertainment: Film
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch quiz questions"}), 500

    data = response.json()
    if data.get("response_code") != 0:
        return jsonify({"error": "API returned an error code"}), 500

    questions = data.get("results", [])
    # Process questions: combine incorrect_answers with correct_answer and shuffle them.
    processed_questions = []
    for q in questions:
        # Unescape HTML entities
        question_text = html.unescape(q.get("question"))
        correct_answer = html.unescape(q.get("correct_answer"))
        incorrect_answers = [html.unescape(ans) for ans in q.get("incorrect_answers")]
        options = incorrect_answers + [correct_answer]
        random.shuffle(options)
        processed_questions.append(
            {
                "question": question_text,
                "options": options,
                "correct_answer": correct_answer,
            }
        )
    # Store the processed questions in the session for later verification
    session["quiz_questions"] = processed_questions
    return render_template("quiz.html", questions=processed_questions)


@app.route("/quiz/submit", methods=["POST"])
def quiz_submit():
    """
    Processes quiz submission, calculates the user's score, and returns the result including
    the correct answers for each question.
    """
    data = request.get_json()
    user_answers = data.get("answers", {})

    # Retrieve stored questions from session
    questions = session.get("quiz_questions")
    if not questions:
        return jsonify({"error": "No quiz questions found"}), 400

    score = 0
    total = len(questions)
    correct_answers = []
    for idx, q in enumerate(questions):
        correct = q.get("correct_answer")
        correct_answers.append(correct)
        if str(idx) in user_answers and user_answers[str(idx)] == correct:
            score += 1

    # Return the result without updating quiz points
    result = {"score": score, "total": total, "correct_answers": correct_answers}
    return jsonify(result), 200


@app.before_request
def before_request():
    """
    Opens the db connection.
    """
    env_path = find_dotenv()
    # print(f"Found .env file at: {env_path}")
    load_dotenv(env_path, override=True)
    g.db = mysql.connector.connect(
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        # mysql is the name of the service in the github action config, so add it as default here for testing only
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=os.getenv("DB_PORT", 3306),
        database=os.getenv("DB_NAME"),
        # auth_plugin='caching_sha2_password'
    )


@app.after_request
def after_request(response):
    """
    Closes the db connection.
    """
    g.db.close()
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
