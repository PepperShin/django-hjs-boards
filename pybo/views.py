from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from pybo.forms import AnswerForm, QuestionForm
from pybo.models import Answer, Question
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.


# http://127.0.0.1:8000/pybo
def index(request):
    # ?page=4
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


from django.http import HttpResponse


def set_cookie_view(request):
    """쿠키 설정"""
    response = HttpResponse("쿠키가 설정되었습니다.")
    response.set_cookie("my_cookie", "cookie_value", max_age=3600)  # 1시간 동안 유지
    return response


def get_cookie_view(request):
    """쿠키 가져오기"""
    cookie_value = request.COOKIES.get("my_cookie", "쿠키가 없습니다.")
    return HttpResponse(f"쿠키 값: {cookie_value}")


def delete_cookie_view(request):
    """쿠키 삭제"""
    response = HttpResponse("쿠키가 삭제되었습니다.")
    response.delete_cookie("my_cookie")
    return response


def set_session_view(request):

    from django.contrib.sessions.models import Session
    from django.contrib.sessions.backends.db import SessionStore

    # 특정 세션 키 조회
    session_key = "845fap6o3dpt4n8bzzx231lc03ctgorm"  # 실제 저장된 session_key 입력
    session = Session.objects.get(session_key=session_key)

    # 세션 데이터 복호화
    session_data = SessionStore(session_key=session_key).load()
    print(session_data)  # {'username': 'DjangoUser'}

    """세션 설정"""
    request.session["username"] = "DjangoUser"  # 세션에 값 저장
    request.session.set_expiry(3600)  # 1시간 후 만료 (기본값: 브라우저 종료 시 삭제)
    return HttpResponse("세션이 설정되었습니다.")


def get_session_view(request):
    """세션 가져오기"""
    username = request.session.get("username", "세션이 없습니다.")
    return HttpResponse(f"세션 값: {username}")


def delete_session_view(request):
    """세션 삭제"""
    request.session.flush()  # 모든 세션 데이터 삭제
    return HttpResponse("세션이 삭제되었습니다.")
