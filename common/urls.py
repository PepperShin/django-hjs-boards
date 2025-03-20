# dev_19
from django.urls import path
from django.contrib.auth import views as auth_view

from common import views

app_name = "common"

urlpatterns = [
    path(
        "login/",
        auth_view.LoginView.as_view(template_name="common/login.html"),
        name="login",
    ),  # dev_13
    path("logout/", views.logout_view, name="logout"),
]
