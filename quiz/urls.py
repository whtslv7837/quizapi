from django.urls import path
from .views import (
    QuizListView, QuizDetailView,
    QuestionListView, AnswerListView,
    UserQuizListView, SubmitQuizView,
)

urlpatterns = [
    path('api/quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('api/quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('api/questions/', QuestionListView.as_view(), name='question-list'),
    path('api/answers/', AnswerListView.as_view(), name='answer-list'),
    path('api/my-results/', UserQuizListView.as_view(), name='user-quiz-list'),
    path('api/quizzes/<int:quiz_id>/submit/', SubmitQuizView.as_view(), name='quiz-submit'),
]
