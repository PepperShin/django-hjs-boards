from django.contrib import admin
from django.urls import include, path
from pybo import views

app_name = "pybo"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),  # dev_3
]
