from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Quiz, Question, Answer, UserQuiz
from .serializers import (
    QuizSerializer,
    QuestionSerializer,
    AnswerSerializer,
    UserQuizSerializer,
    QuizSubmissionSerializer
)


# Quiz: List + Retrieve
class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [AllowAny]


class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [AllowAny]


# Question: List all
class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        quiz_id = self.request.query_params.get('quiz_id')
        if quiz_id:
            return Question.objects.filter(quiz_id=quiz_id)
        return Question.objects.all()


# Answer: List all
class AnswerListView(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        question_id = self.request.query_params.get('question_id')
        if question_id:
            return Answer.objects.filter(question_id=question_id)
        return Answer.objects.all()


# UserQuiz: List only results of current user
class UserQuizListView(generics.ListAPIView):
    serializer_class = UserQuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserQuiz.objects.filter(user=self.request.user)


# Submit quiz answers
class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        serializer = QuizSubmissionSerializer(data=request.data, context={'quiz_id': quiz_id})
        if serializer.is_valid():
            answers = serializer.validated_data['answers']
            score = 0

            for item in answers:
                answer = Answer.objects.get(id=item['answer_id'])
                if answer.is_correct:
                    score += 1

            user_quiz = UserQuiz.objects.create(
                user=request.user,
                quiz_id=quiz_id,
                score=score
            )

            return Response({
                "score": score,
                "total": len(answers),
                "quiz": QuizSerializer(user_quiz.quiz).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
