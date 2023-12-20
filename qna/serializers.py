from rest_framework import serializers
from .models import Question, Answer, User


class QuestionSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source="author.name")

    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'author_name', 'created_at']

class AnswerSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source="author.name")
    question_title = serializers.ReadOnlyField(source="question.title")
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Answer
        fields = ['id', 'question', 'question_title', 'content', 'author', 'author_name', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    # related_name을 사용하여 역참조
    questions = QuestionSerializer(many=True, read_only=True) #역방향 관계
    answers = AnswerSerializer(many=True, read_only=True) #역방향 관계

    class Meta:
        model = User
        fields = ['id', 'student_id', 'name', 'email', 'division', 'questions', 'answers']

