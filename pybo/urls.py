from django.contrib import admin
from django.urls import include, path

from pybo.views import base_views, question_views, answer_views


app_name = "pybo"

## http://127.0.0.1:8000/pybo/5/
urlpatterns = [
    path("", base_views.index, name="index"),
    # http://127.0.0.1:8000/pybo/<int:question_id>/
    path("<int:question_id>/", base_views.detail, name="detail"),  #  dev_3
    path(
        "answer/create/<int:question_id>/",
        answer_views.answer_create,
        name="answer_create",
    ),  # dev_5
    path(
        "question/create/", question_views.question_create, name="question_create"
    ),  # dev_6
    path(
        "question/modify/<int:question_id>/",
        question_views.question_modify,
        name="question_modify",
    ),  # dev_17
    path(
        "question/delete/<int:question_id>/",
        question_views.question_delete,
        name="question_delete",
    ),  # dev_17
    path(
        "answer/modify/<int:answer_id>/",
        answer_views.answer_modify,
        name="answer_modify",
    ),  # dev_18
    path(
        "answer/delete/<int:answer_id>/",
        answer_views.answer_delete,
        name="answer_delete",
    ),  # dev_18
    path(
        "question/vote/<int:question_id>/",
        question_views.question_vote,
        name="question_vote",
    ),  # dev_19
    path(
        "answer/vote/<int:answer_id>/",
        answer_views.answer_vote,
        name="answer_vote",
    ),  # dev_19
]
