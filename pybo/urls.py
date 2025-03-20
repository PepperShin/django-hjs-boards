from django.contrib import admin
from django.urls import include, path
from pybo import views

app_name = "pybo"

## http://127.0.0.1:8000/pybo/5/
urlpatterns = [
    path("", views.index, name="index"),
    # http://127.0.0.1:8000/pybo/<int:question_id>/
    path("<int:question_id>/", views.detail, name="detail"),  #  dev_3
    path(
        "answer/create/<int:question_id>/", views.answer_create, name="answer_create"
    ),  # dev_5
    # <a href="{% url 'pybo:question_create' %}" class="btn btn-primary">질문 등록하기</a>
    path("question/create/", views.question_create, name="question_create"),  # dev_9
    # dev_14
    path("set-cookie/", views.set_cookie_view, name="set_cookie"),
    path("get-cookie/", views.get_cookie_view, name="get_cookie"),
    path("delete-cookie/", views.delete_cookie_view, name="delete_cookie"),
    path("set-session/", views.set_session_view, name="set_session"),
    path("get-session/", views.get_session_view, name="get_session"),
    path("delete-session/", views.delete_session_view, name="delete_session"),
]
