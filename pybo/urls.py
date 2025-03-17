from django.contrib import admin
from django.urls import include, path

from pybo import views

urlpatterns = [
    path("", views.index),
    path("<int:question_id>/", views.detail),  # dev_3
]
