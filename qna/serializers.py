from rest_framework import serializers
from .models import Question, Answer, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'student_id', 'name', 'email', 'division']


class QuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'author', 'created_at']


class AnswerSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'content', 'author', 'created_at']
