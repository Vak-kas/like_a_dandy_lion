from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    student_id = models.IntegerField(help_text="Student ID", unique=True)
    name = models.CharField(help_text="Name", max_length=100)
    email = models.EmailField()
    division = models.CharField(help_text="front or back or admin", max_length=100)

class Question(models.Model):
    # 질문 제목
    title = models.CharField(max_length=200, verbose_name='제목')
    # 질문 내용
    content = models.TextField(verbose_name='내용')
    # 작성자는 장고의 내장 User 모델을 외래키로 사용
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    # 생성 시간
    created_at = models.DateTimeField(verbose_name='생성 시간')
    class Meta:
        verbose_name = 'QnA'
        verbose_name_plural = 'QnA'

    def __str__(self):
        return self.title

class Answer(models.Model):
    # 질문 - Answer가 Question에 연결됩니다.
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='질문')
    # 답변 내용
    content = models.TextField(verbose_name='내용')
    # 작성자
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    # 생성 시간
    created_at = models.DateTimeField(default=timezone.now,verbose_name='생성 시간')

    class Meta:
        verbose_name = '답변'
        verbose_name_plural = '답변'

    def __str__(self):
        return f"{self.author}'s answer to {self.question.title}"


