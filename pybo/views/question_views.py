from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from pybo.forms import AnswerForm, QuestionForm
from pybo.models import Answer, Question
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages as message

from django.contrib.auth.decorators import login_required


@login_required(login_url="common:login")
def question_create(request):

    print(request.POST.get("content"))

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # dev_16
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:index")

    else:
        form = QuestionForm()

    context = {"form": form}
    return render(request, "pybo/question_form.html", context)


# dev_17
# 글 수정
@login_required(login_url="common:login")
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        message.error(
            request, "수정 권한이 없습니다."
        )  # request 객체 안에 뒤 인자의 값을 집어넣는 함수
        return redirect("pybo:detail", question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = QuestionForm(instance=question)

    context = {"form": form}
    return render(request, "pybo/question_form.html", context)


# 글 삭제
@login_required(login_url="common:login")
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        message.error(request, "삭제권한이 없습니다")
        return redirect("pybo:detail", question_id=question_id)

    question.delete()
    return redirect("pybo:index")


# 추천
@login_required(login_url="common:login")
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user == question.author:
        message.error(request, "본인의 개시물에는 추천할 수 없습니다.")
    else:
        question.voter.add(request.user)

    return redirect("pybo:detail", question_id=question.id)
