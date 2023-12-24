from rest_framework import serializers
from .models import Question, Answer, User


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['student_id', 'name', 'email', 'division']

class QuestionSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()

    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'author', 'created_at', "modified_at"]

class AnswerSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()  # 커스텀 UserSerializer 사용
    question_title = serializers.ReadOnlyField(source="question.title")

    class Meta:
        model = Answer
        fields = ['id', 'question', 'question_title', 'content', 'author', 'created_at', "modified_at"]



class UserSerializer(serializers.ModelSerializer):
    # related_name을 사용하여 역참조
    questions = QuestionSerializer(many=True, read_only=True) #역방향 관계
    answers = AnswerSerializer(many=True, read_only=True) #역방향 관계

    class Meta:
        model = User
        fields = ['student_id', 'name', 'email', 'division', 'questions', 'answers']



