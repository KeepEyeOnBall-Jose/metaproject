import pytest
from fastapi.testclient import TestClient
from main import app, load_questions

client = TestClient(app)


def test_get_questions():
    response = client.get("/questions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Verify we have actual questions loaded
    assert len(data) > 0
    # Check structure of first question
    if data:
        question = data[0]
        assert "id" in question
        assert "question" in question
        assert "category" in question
        assert "status" in question


def test_get_categories():
    response = client.get("/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # Verify we have categories
    assert len(data) > 0
    # All values should be integers (counts)
    for count in data.values():
        assert isinstance(count, int)
        assert count > 0


def test_get_question_not_found():
    response = client.get("/questions/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Question not found"}


def test_load_questions_function():
    """Test the load_questions function directly"""
    questions = load_questions()
    assert isinstance(questions, list)
    assert len(questions) > 0
    # Verify structure
    for q in questions:
        assert hasattr(q, "id")
        assert hasattr(q, "question")
        assert hasattr(q, "category")
        assert hasattr(q, "status")
        assert hasattr(q, "created_at")


def test_categories_match_questions():
    """Test that categories endpoint matches the questions data"""
    questions_response = client.get("/questions")
    categories_response = client.get("/categories")

    questions = questions_response.json()
    categories = categories_response.json()

    # Manually count categories from questions
    expected_categories = {}
    for q in questions:
        cat = q["category"]
        expected_categories[cat] = expected_categories.get(cat, 0) + 1

    assert categories == expected_categories


def test_get_specific_question():
    """Test getting a specific question by ID"""
    # First get all questions
    response = client.get("/questions")
    questions = response.json()
    assert len(questions) > 0

    # Get the first question's ID
    first_question = questions[0]
    question_id = first_question["id"]

    # Get that specific question
    response = client.get(f"/questions/{question_id}")
    assert response.status_code == 200
    specific_question = response.json()

    # Should match the first question
    assert specific_question == first_question
