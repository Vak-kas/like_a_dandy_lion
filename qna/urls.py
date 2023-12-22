from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet

app_name = 'qna'


router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', views.index, name = "index"),
    path('', include(router.urls)),
    path('<int:question_id>/', views.detail, name="detail"),
    path('<int:question_id>/answer/create/', views.AnswerCreateAPIView.as_view(), name='answer_create_api'),
    path('<int:question_id>/answer/', views.get_answers_for_question, name='get_answers_for_question')
]