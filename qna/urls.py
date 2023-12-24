from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet
from . import views

app_name = 'qna'

# 라우터 생성 및 ViewSet 등록
router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'questions/(?P<question_id>\d+)/answers', views.AnswerViewSet, basename='answer')

urlpatterns = [
    path('', include(router.urls)),
]
