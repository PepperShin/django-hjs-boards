from django import forms

from pybo.models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # form과 모델을 연걸
        fields = ["subject", "content"]  # QuestionForm에서 사용할 Question 모델의 속성
