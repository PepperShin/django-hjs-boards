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
]
