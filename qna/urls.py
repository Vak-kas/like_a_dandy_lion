from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet, AnswerDeleteAPIView

app_name = 'qna'


router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', views.index, name = "index"),
    path('', include(router.urls)),
    path('<int:question_id>/', views.detail, name="detail"),
    path('<int:question_id>/answer/create/', views.AnswerCreateAPIView.as_view(), name='answer_create_api'), #답변 생성
    path('<int:question_id>/answer/', views.get_answers_for_question, name='get_answers_for_question'), #답변 조회
    path('<int:question_id>/answer/<int:answer_id>/delete/', AnswerDeleteAPIView.as_view(), name='answer_delete'),
    path('question/', views.QuestionListAPIView.as_view(), name='question_list_api'), #질문 조회
    path('question/create/', views.QuestionCreateAPIView.as_view(), name="question_create_api"), #질문 생성

]