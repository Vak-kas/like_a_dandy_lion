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
    path('answer/create/<int:question_id>/', views.answer_create, name="answer_create"),
    path('questions/<int:question_id>/answers/', views.get_answers_for_question, name='get_answers_for_question')
]