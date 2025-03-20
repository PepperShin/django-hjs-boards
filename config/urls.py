from django.contrib import admin
from django.urls import include, path

from pybo import views


# http://127.0.0.1:8000/
urlpatterns = [
    path("admin/", admin.site.urls),  # http://127.0.0.1:8000
    path("pybo/", include("pybo.urls")),
    path("common/", include("common.urls")),  # dev_13
    path("", views.index, name="index"),  # dev_13
]
