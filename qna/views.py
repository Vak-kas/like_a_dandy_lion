from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .models import Question, Answer, User
from rest_framework import viewsets, status
from .serializers import QuestionSerializer, AnswerSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from django.utils import timezone
from rest_framework.decorators import action







# # Create your views here.
#질문 조회
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 로그인한 사용자만 수정 가능하게

    # 질문 생성

    def create(self, request, *args, **kwargs):
        # 클라이언트로부터 받은 데이터
        data = request.data

        # 클라이언트에서 제공한 student_id를 사용하여 User 객체를 찾습니다.
        student_id = data.get('student_id')
        try:
            user = User.objects.get(student_id=student_id)
        except User.DoesNotExist:
            return Response({"error": "User with the given student_id does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        # 새 Question 객체를 생성하고 User 객체를 연결합니다.
        question = Question(title=data.get('title'), content=data.get('content'), author=user)

        # Question 객체를 저장합니다.
        question.save()

        # 저장된 Question 객체의 정보를 반환합니다.
        return Response({"message": "Question created successfully", "question": {
            "title": question.title,
            "content": question.content,
            "student_id": user.student_id,
            "created_at": question.created_at,
        }}, status=status.HTTP_201_CREATED)


    #질문 삭제
    def destroy(self, request, *args, **kwargs):
        print("삭제 요청이 들어왔음")
        student_id = request.query_params.get('student_id')  # 학번 정보를 요청의 쿼리 파라미터로부터 얻어옴
        print(student_id)

        try:
            # student_id를 사용하여 User 객체 찾기
            user = User.objects.get(student_id=student_id)
        except User.DoesNotExist: #User 객체 존재하지 않다면?
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        print(user)
        try:
            # URL에서 제공된 pk를 사용하여 Question 객체를 찾기
            question = Question.objects.get(pk=kwargs['pk'])
        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=status.HTTP_404_NOT_FOUND)


        # User가 Question의 작성자와 일치하는지 확인
        if question.author == user:
            question.delete()  # 조건이 충족되면 질문을 삭제
            return Response({"message": "Question deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            # 작성자가 일치하지 않으면 오류 메시지를 반환
            return Response({"error": "You do not have permission to delete this question."},
                            status=status.HTTP_403_FORBIDDEN)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        answers = Answer.objects.filter(question=instance)
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['answers'] = AnswerSerializer(answers, many=True).data
        return Response(data)

    def update(self, request, *args, **kwargs):
        # 클라이언트로부터 받은 데이터
        data = request.data

        # 클라이언트에서 제공한 student_id를 사용하여 User 객체를 찾습니다.
        student_id = data.get('student_id')
        try:
            user = User.objects.get(student_id=student_id)
        except User.DoesNotExist:
            return Response({"error": "주어진 학번을 가진 사용자가 존재하지 않습니다."},
                            status=status.HTTP_404_NOT_FOUND)

        # URL에서 제공된 question_id를 사용하여 해당 질문을 찾기
        question_id = kwargs.get('pk')
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return Response({"error": "질문을 찾을 수 없습니다."},
                            status=status.HTTP_404_NOT_FOUND)

        # 질문 작성자와 현재 사용자가 일치하는지 확인
        if question.author == user:
            # 권한이 있는 경우 질문 내용 업데이트
            question.title = data.get('title')
            question.content = data.get('content')
            question.modified_at = timezone.now()  # modified_at 필드 업데이트
            question.save()
            return Response({"message": "질문이 성공적으로 수정되었습니다."}, status=status.HTTP_200_OK)
        else:
            # 작성자가 일치하지 않으면 오류 메시지를 반환
            return Response({"error": "이 질문을 수정할 권한이 없습니다."},
                            status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        # student_id 파라미터를 받아옴
        student_id = request.query_params.get('student_id')

        # student_id가 존재하면 해당 사용자의 질문 목록만 필터링
        if student_id:
            queryset = Question.objects.filter(author__student_id=student_id)
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        # 클라이언트로부터 받은 데이터
        data = request.data

        # 클라이언트에서 제공한 student_id를 사용하여 User 객체를 찾습니다.
        student_id = data.get('student_id')
        try:
            user = User.objects.get(student_id=student_id)
        except User.DoesNotExist:
            return Response({"error": "User with the given student_id does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        # URL에서 제공된 question_id를 사용하여 해당 질문을 찾기
        question_id = kwargs.get('question_id')
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found."},
                            status=status.HTTP_404_NOT_FOUND)

        # 새 Answer 객체를 생성하고 User와 Question 객체를 연결합니다.
        answer = Answer(content=data.get('content'), author=user, question=question)

        # Answer 객체를 저장합니다.
        answer.save()

        # 저장된 Answer 객체의 정보를 반환합니다.
        return Response({"message": "Answer created successfully", "answer": {
            "content": answer.content,
            "student_id": user.student_id,
            "created_at": answer.created_at,
        }}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        # 클라이언트로부터 받은 데이터


        # 클라이언트에서 제공한 student_id를 사용하여 User 객체를 찾기
        student_id = request.query_params.get('student_id')

        student_id = request.query_params.get('student_id')

        # 클라이언트에서 제공한 student_id를 사용하여 User 객체를 찾기
        # student_id = data.get('student_id')

        try:
            user = User.objects.get(student_id=student_id)
        except User.DoesNotExist:
            return Response({"error": "User with the given student_id does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        # URL에서 제공된 answer_id를 사용하여 해당 답변을 찾기
        answer_id = kwargs.get('pk')
        try:
            answer = Answer.objects.get(pk=answer_id)
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found."},
                            status=status.HTTP_404_NOT_FOUND)

        # 답변 작성자와 현재 사용자가 일치하는지 확인
        if answer.author == user:
            answer.delete()  # 조건이 충족되면 답변을 삭제
            return Response({"message": "Answer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            # 작성자가 일치하지 않으면 오류 메시지를 반환
            return Response({"error": "You do not have permission to delete this answer."},
                            status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        # 클라이언트로부터 받은 데이터
        data = request.data
        print(data)

        # 클라이언트에서 제공한 student_id를 사용하여 User 객체를 찾습니다.
        student_id = data.get('student_id')
        print(student_id)
        try:
            user = User.objects.get(student_id=student_id)
        except User.DoesNotExist:
            return Response({"error": "User with the given student_id does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        # URL에서 제공된 answer_id를 사용하여 해당 답변을 찾기
        answer_id = kwargs.get('pk')
        print(answer_id)
        try:
            answer = Answer.objects.get(pk=answer_id)
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found."},
                            status=status.HTTP_404_NOT_FOUND)
        print(answer.content)
        # 답변 작성자와 현재 사용자가 일치하는지 확인
        if answer.author == user:
            # 권한이 있는 경우 답변 내용 업데이트
            answer.content = data.get('content')
            answer.modified_at = timezone.now()  # Update modified_at field
            answer.save()
            print(answer.content)
            return Response({"message": "Answer updated successfully"}, status=status.HTTP_200_OK)
        else:
            # 작성자가 일치하지 않으면 오류 메시지를 반환
            return Response({"error": "You do not have permission to update this answer."},
                            status=status.HTTP_403_FORBIDDEN)


    def retrieve(self, request, *args, **kwargs):
        # 클라이언트로부터 받은 데이터


        # 클라이언트에서 제공한 student_id를 사용하여 User 객체를 찾기

        # URL에서 제공된 answer_id를 사용하여 해당 답변을 찾기
        answer_id = kwargs.get('pk')
        # print(answer_id)
        try:
            answer = Answer.objects.get(pk=answer_id)
        except Answer.DoesNotExist:
            return Response({"error": "Answer not found."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = AnswerSerializer(answer)
        return Response(serializer.data, status=status.HTTP_200_OK)


