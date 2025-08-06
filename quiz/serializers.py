from rest_framework import serializers
from .models import Quiz, Question, Answer, UserQuiz


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'questions']


class UserQuizSerializer(serializers.ModelSerializer):
    quiz = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = UserQuiz
        fields = ['id', 'user', 'quiz', 'score', 'completed_at']


class QuizAnswerSubmissionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField()


class QuizSubmissionSerializer(serializers.Serializer):
    answers = QuizAnswerSubmissionSerializer(many=True)

    def validate(self, data):
        quiz_id = self.context['quiz_id']
        for item in data['answers']:
            try:
                question = Question.objects.get(id=item['question_id'], quiz_id=quiz_id)
                answer = Answer.objects.get(id=item['answer_id'], question=question)
            except (Question.DoesNotExist, Answer.DoesNotExist):
                raise serializers.ValidationError("Invalid question or answer.")
        return data
