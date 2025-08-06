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
    return Question.objects.create(quiz=quiz, text="Sample question?")

@pytest.fixture
def correct_answer(db, question):
    return Answer.objects.create(question=question, text="Correct", is_correct=True)

@pytest.fixture
def user_quiz(db, user, quiz):
    return UserQuiz.objects.create(user=user, quiz=quiz, score=1)
