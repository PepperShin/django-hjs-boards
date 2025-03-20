from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from pybo.forms import AnswerForm, QuestionForm
from pybo.models import Answer, Question
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.


# http://127.0.0.1:8000/pybo
def index(request):
    #?page=4
    page = request.GET.get("page", "1")  # 페이지
    
    question_list = Question.objects.order_by("-create_date")
    
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {"question_list": page_obj}

    return render(request, "pybo/question_list.html", context)


# http://127.0.0.1:8000/pybo/<int:question_id>/
def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)

    context = {"question": question}
    return render(request, "pybo/question_detail.html", context)

    # path(
    #     "answer/create/<int:question_id>/", views.answer_create, name="answer_create"
    # ),  # dev_5


# dev_9
def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("pybo:detail", question_id=question.id)

    else:
        return HttpResponseNotAllowed("Only POST is possible.")

    context = {"question": question, "form": form}
    return render(request, "pybo/question_detail.html", context)


def question_create(request):

    print(request.POST.get("content"))

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:index")

    else:
        form = QuestionForm()

    context = {"form": form}
    return render(request, "pybo/question_form.html", context)
