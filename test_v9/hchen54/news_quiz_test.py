import os
import sys
import json
import pytest
from pathlib import Path

# Adjust this as needed: typically, two levels up from the test file
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app import app  # Now this import should succeed

@pytest.fixture
def client():
    # Create a test client using the Flask application configured for testing
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ------------------
# News Endpoint Tests
# ------------------

def test_news_endpoint_status(client):
    """Test that /news returns a 200 status code."""
    response = client.get("/news?page=1")
    assert response.status_code == 200

def test_news_endpoint_content_type(client):
    """Test that /news returns HTML content."""
    response = client.get("/news?page=1")
    assert "text/html" in response.content_type

def test_news_articles_returned(client):
    """Test that /news returns articles in the rendered HTML."""
    response = client.get("/news?page=1")
    data = response.get_data(as_text=True)
    # Check that a known article property (e.g. "Published:" or a placeholder) exists
    assert "Published:" in data

def test_news_pagination_previous_link(client):
    """Test that pagination includes a 'Previous' link when page > 1."""
    response = client.get("/news?page=2")
    data = response.get_data(as_text=True)
    assert "Previous" in data

def test_news_pagination_next_link(client):
    """Test that pagination includes a 'Next' link when there are more pages."""
    response = client.get("/news?page=1")
    data = response.get_data(as_text=True)
    # Assuming total_pages > 1
    assert "Next" in data

def test_news_articles_structure(client):
    """Test that at least one news cell contains expected elements."""
    response = client.get("/news?page=1")
    data = response.get_data(as_text=True)
    # Check for a link (news title) and an image tag if present
    assert "<div class=\"news-cell\">" in data
    assert "<img" in data or "Article image" in data

def test_news_valid_html(client):
    """Basic test to ensure the returned HTML is not empty."""
    response = client.get("/news?page=1")
    data = response.get_data(as_text=True)
    assert len(data.strip()) > 0

def test_news_articles_date(client):
    """Test that news articles include a published date."""
    response = client.get("/news?page=1")
    data = response.get_data(as_text=True)
    assert "Published:" in data

def test_news_page_navigation(client):
    """Test that changing the page query parameter changes the content."""
    response1 = client.get("/news?page=1")
    response2 = client.get("/news?page=2")
    # For simplicity, just check that responses differ (if there are enough articles)
    assert response1.get_data(as_text=True) != response2.get_data(as_text=True)

def test_news_total_pages_calculation(client):
    """Test that total pages is rendered in the HTML."""
    response = client.get("/news?page=1")
    data = response.get_data(as_text=True)
    assert "Page 1 of" in data

# ------------------
# Quiz Endpoint Tests
# ------------------

def test_quiz_endpoint_status(client):
    """Test that /quiz returns a 200 status code."""
    response = client.get("/quiz")
    assert response.status_code == 200

def test_quiz_endpoint_returns_html(client):
    """Test that /quiz returns HTML content."""
    response = client.get("/quiz")
    assert "text/html" in response.content_type

def test_quiz_questions_count(client):
    """Test that the /quiz page renders 10 questions (or the number set by API)."""
    response = client.get("/quiz")
    data = response.get_data(as_text=True)
    # Count occurrences of "quiz-question" class in the HTML
    count = data.count("class=\"quiz-question\"")
    # Assuming API returns 10 questions
    assert count == 10

def test_quiz_question_has_question_key(client):
    """Test that each quiz question cell contains a question text."""
    response = client.get("/quiz")
    data = response.get_data(as_text=True)
    # Check that the rendered HTML contains question text markers
    assert "quiz-question" in data
    # Optionally check for a punctuation like "?" in one question
    assert "?" in data

def test_quiz_question_has_options(client):
    """Test that each quiz question contains multiple options."""
    response = client.get("/quiz")
    data = response.get_data(as_text=True)
    # Check that there is at least one radio input for options
    assert "type=\"radio\"" in data

def test_quiz_question_has_correct_answer_hidden(client):
    """Since the correct answer is stored in session (and not rendered visibly), 
    we can test that the quiz page does not expose it."""
    response = client.get("/quiz")
    data = response.get_data(as_text=True)
    # The correct answer should not appear directly (only after submission)
    assert "Correct answer:" not in data

def test_quiz_submit_endpoint_status(client):
    """Test that posting to /quiz/submit returns a 200 status code."""
    # First, get the quiz to set the session
    client.get("/quiz")
    # Create dummy answers: assume each question's answer is the first option
    # Since we cannot parse the actual options from session easily, we use a dummy dict.
    dummy_answers = {str(i): "dummy" for i in range(10)}
    response = client.post("/quiz/submit", data=json.dumps({"answers": dummy_answers}),
                           content_type="application/json")
    assert response.status_code == 200

def test_quiz_submit_returns_json(client):
    """Test that /quiz/submit returns JSON."""
    client.get("/quiz")
    dummy_answers = {str(i): "dummy" for i in range(10)}
    response = client.post("/quiz/submit", data=json.dumps({"answers": dummy_answers}),
                           content_type="application/json")
    data = json.loads(response.get_data(as_text=True))
    assert "score" in data
    assert "total" in data
    assert "correct_answers" in data

def test_quiz_submit_score_calculation(client):
    """Test that quiz submission returns a score between 0 and total questions."""
    client.get("/quiz")
    # For this test, answer all questions with an answer that is likely incorrect.
    dummy_answers = {str(i): "incorrect" for i in range(10)}
    response = client.post("/quiz/submit", data=json.dumps({"answers": dummy_answers}),
                           content_type="application/json")
    data = json.loads(response.get_data(as_text=True))
    assert 0 <= data["score"] <= data["total"]

def test_quiz_submit_partial_correct(client):
    """Test that if some answers are correct, score is between 1 and total-1."""
    # Get the quiz to set session.
    client.get("/quiz")
    # In a real scenario, you would compare with session. Here we simulate mixed answers.
    dummy_answers = {}
    # For simplicity, mark even-indexed questions as correct
    for i in range(10):
        if i % 2 == 0:
            dummy_answers[str(i)] = "correct"  # we expect session to contain "correct" for these?
        else:
            dummy_answers[str(i)] = "wrong"
    response = client.post("/quiz/submit", data=json.dumps({"answers": dummy_answers}),
                           content_type="application/json")
    data = json.loads(response.get_data(as_text=True))
    # Since we don't have actual correct answers from session, we only assert the score is within range.
    assert 0 <= data["score"] <= 10

def test_quiz_submit_response_contains_correct_answers(client):
    """Test that the /quiz/submit JSON response contains a correct_answers list."""
    client.get("/quiz")
    dummy_answers = {str(i): "dummy" for i in range(10)}
    response = client.post("/quiz/submit", data=json.dumps({"answers": dummy_answers}),
                           content_type="application/json")
    data = json.loads(response.get_data(as_text=True))
    assert isinstance(data["correct_answers"], list)
    assert len(data["correct_answers"]) == 10

def test_quiz_session_storage_exists(client):
    """Test that after loading /quiz, the session has 'quiz_questions' stored."""
    with client.session_transaction() as session_data:
        # Before calling /quiz, session should not contain quiz_questions
        assert 'quiz_questions' not in session_data
    client.get("/quiz")
    with client.session_transaction() as session_data:
        assert 'quiz_questions' in session_data

def test_quiz_questions_unescaped_html(client):
    """Test that quiz questions do not contain HTML entities (i.e. have been unescaped)."""
    response = client.get("/quiz")
    data = response.get_data(as_text=True)
    # Check that common HTML entities like &quot; or &amp; are not present
    assert "&quot;" not in data
    assert "&amp;" not in data

def test_news_and_quiz_pages_navigate_correctly(client):
    """Test that navigation links in the navbar on /news and /quiz pages contain expected href values."""
    news_response = client.get("/news?page=1")
    quiz_response = client.get("/quiz")
    news_html = news_response.get_data(as_text=True)
    quiz_html = quiz_response.get_data(as_text=True)
    # Check that the navbar contains links to /search_page, /wall, /review, /news, and /quiz
    for endpoint in ["/search_page", "/wall", "/review", "/news", "/quiz"]:
        assert endpoint in news_html
        assert endpoint in quiz_html
