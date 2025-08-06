from django.contrib import admin
from .models import Quiz, Question, Answer, UserQuiz


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct',)


@admin.register(UserQuiz)
class UserQuizAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'completed_at')
    list_filter = ('quiz', 'completed_at')
    search_fields = ('user__username',)
