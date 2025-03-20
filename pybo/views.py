from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from pybo.forms import AnswerForm, QuestionForm
from pybo.models import Question
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.


# http://127.0.0.1:8000/pybo/
def index(request):

    page = request.GET.get("page", "1")  # 페이지 넘어오는게 없으면 1번이 디폴트

    question_list = Question.objects.order_by("-create_date")

    # from django.core.paginator import Paginator
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {"question_list": page_obj}
    # context = {"question_list": question_list}
    return render(request, "pybo/question_list.html", context)


def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(
        Question, pk=question_id
    )  # 페이지를 404로 바꿔주는 함수
    context = {"question": question}
    return render(request, "pybo/question_detail.html", context)


def answer_create(request, question_id):  # dev_9
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question  # question 객체 입력
            answer.save()
            return redirect("pybo:detail", question_id=question.id)

    else:
        return HttpResponseNotAllowed("Only Post is possible")

    context = {"question": question, "form": form}
    return render(request, "pybo/question_detail.html", context)


# path("question/create/", views.question_create, name="question_create"),
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():  # form 태그로 받은 데이터 유효성 검사
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:index")

    else:
        form = QuestionForm()

    context = {"form": form}
    return render(request, "pybo/question_form.html", context)
