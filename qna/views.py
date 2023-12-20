from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Question
# Create your views here.
def index(request):
    #목록 출력
    question_list = Question.objects.order_by("-created_at");
    context = {'question_list' : question_list}
    return render(request, 'question_list.html', context);


def detail(request, question_id):
    #내용 출력
    question = get_object_or_404(Question, pk = question_id)
    context = {'question' : question }
    return render(request, 'question_detail.html', context);
