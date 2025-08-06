import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from quiz.models import Quiz, Question, Answer, UserQuiz


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def quiz(db):
    return Quiz.objects.create(title="Sample Quiz", description="Just a test")


@pytest.fixture
def question(db, quiz):
    return Question.objects.create(quiz=quiz, text="What is 2 + 2?")


@pytest.fixture
def correct_answer(db, question):
    return Answer.objects.create(question=question, text="4", is_correct=True)


@pytest.fixture
def incorrect_answer(db, question):
    return Answer.objects.create(question=question, text="5", is_correct=False)


@pytest.fixture
def user_quiz(db, user, quiz):
    return UserQuiz.objects.create(user=user, quiz=quiz, score=1)


@pytest.mark.django_db
def test_list_quizzes(api_client, quiz):
    response = api_client.get("/api/quizzes/")
    assert response.status_code == 200
    assert any(q["id"] == quiz.id for q in response.data)


@pytest.mark.django_db
def test_retrieve_quiz(api_client, quiz, question, correct_answer):
    response = api_client.get(f"/api/quizzes/{quiz.id}/")
    assert response.status_code == 200
    assert response.data["id"] == quiz.id
    assert "questions" in response.data
    assert len(response.data["questions"]) == 1


@pytest.mark.django_db
def test_list_questions(api_client, question):
    response = api_client.get("/api/questions/")
    assert response.status_code == 200
    assert any(q["id"] == question.id for q in response.data)


@pytest.mark.django_db
def test_list_answers(api_client, correct_answer, incorrect_answer):
    response = api_client.get("/api/answers/")
    assert response.status_code == 200
    assert any(a["id"] == correct_answer.id for a in response.data)


@pytest.mark.django_db
def test_quiz_submission(api_client, user, quiz, question, correct_answer):
    api_client.force_authenticate(user=user)
    data = {
        "answers": [
            {"question_id": question.id, "answer_id": correct_answer.id}
        ]
    }
    response = api_client.post(f"/api/quizzes/{quiz.id}/submit/", data, format="json")
    assert response.status_code == 200 or response.status_code == 201
    assert "score" in response.data
    assert response.data["score"] == 1


@pytest.mark.django_db
def test_user_quiz_results(api_client, user, user_quiz):
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/my-results/")
    assert response.status_code == 200
    assert any(r["id"] == user_quiz.id for r in response.data)
