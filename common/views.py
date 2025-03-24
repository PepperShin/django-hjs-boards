from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate

from common.forms import UserForm


# Create your views here.
def logout_view(request):
    logout(request)
    return redirect("index")


def signup(request):
    if request.method == "POST":
        """
        request.POST.get("username")
        request.POST.get("password1")
        request.POST.get("password2")
        """
        form = UserForm(request.POST)  # from common.forms import UserForm

        if form.is_valid():  # 유효성 검사
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)  # 로그인

            return redirect("index")

    else:
        form = UserForm()

    return render(request, "common/signup.html", {"form": form})
