from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .forms import AnswerForm
from .models import Question, Answer, User
from rest_framework import viewsets
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.http import Http404, JsonResponse


from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
# Create your views here.
#질문 조회
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

#답변조회
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

#답변 생성
class AnswerCreateAPIView(generics.CreateAPIView):
    serializer_class = AnswerSerializer

    def create(self, request, question_id):
        # 입력 데이터에서 필요한 정보 추출
        content = request.data.get('content')
        author_id = request.data.get('author')  # 로그인된 사용자의 학번

        # 해당 질문 객체 가져오기
        question = Question.objects.get(pk=question_id)


        # 사용자 객체 가져오기 (학번으로 검색)
        author = User.objects.get(student_id=author_id)

        # 답변 객체 생성 및 저장
        answer = Answer(content=content, author=author, question=question)
        answer.save()

        # 생성된 답변 정보를 응답으로 반환
        serializer = AnswerSerializer(answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#답변 조회
@api_view(['GET'])
def get_answers_for_question(request, question_id):
    try:
        answers = Answer.objects.filter(question_id=question_id)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)
    except Answer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

#질문 조회
class QuestionListAPIView(generics.ListAPIView):
        queryset = Question.objects.all()
        serializer_class = QuestionSerializer


#질문 생성
class QuestionCreateAPIView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        # POST 요청에서 제목, 내용, 작성자 학번 추출
        title = self.request.data.get('title')
        content = self.request.data.get('content')
        student_id = self.request.data.get('author')
        user = User.objects.get(student_id=student_id)

        # question 모델 생성
        question = Question(title=title, content=content, author=user)
        question.save()

        # serializer를 사용하여 데이터 저장
        serializer = self.get_serializer(question)


        return Response(serializer.data, status=status.HTTP_201_CREATED)


#답변 삭제
class AnswerDeleteAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def delete(self, request, question_id, answer_id):
        try:
            answer = Answer.objects.get(pk=answer_id, author=request.user)
            answer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Answer.DoesNotExist:
            return Response({'error': '글 작성자만 글을 지울 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)



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
            answer.author = request.user;

            #임시 test
            # answer.author = User.objects.get(id=20201738)
            answer.question = question;
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('qna:detail', question_id=question.id), answer.id));
    else:
        form = AnswerForm()
    context = {'form': form, 'question': question}
    return render(request, 'question_detail.html', context)











