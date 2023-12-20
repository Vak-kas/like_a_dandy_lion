from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .forms import AnswerForm
from .models import Question, Answer, User
from rest_framework import viewsets
from .serializers import QuestionSerializer, AnswerSerializer
# Create your views here.
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer



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


# @login_required
def answer_create(request, question_id):
    #답변 등록
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            # answer.author = request.user;

            #임시 test
            answer.author = User.objects.get(id=1)
            answer.question = question;
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('qna:detail', question_id=question.id), answer.id));
    else:
        form = AnswerForm()
    context = {'form': form, 'question': question}
    return render(request, 'question_detail.html', context)







