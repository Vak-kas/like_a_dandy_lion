from django import forms
from qna.models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question;
        fields = ['title', 'content']

        labels = {
            'title' : "제목",
            "content" : "내용",
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer;
        fields = ['content'];
        labels = {
            'content' : "답변내용",
        }
