from django import forms

from pybo.models import Answer, Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # form과 모델을 연걸
        fields = ["subject", "content"]  # QuestionForm에서 사용할 Question 모델의 속성


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["content"]  # foreign키는 따로 빼지 않는다.
        labels = {"content": "답변내용"}
