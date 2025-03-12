from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse(
        "<h1>안녕하세요. 게시판을 만들겠습니다.</h1> </br>게시판을 만들겠습니다."
    )


def hello(request):
    return HttpResponse("<h1>hello world</h1>")
