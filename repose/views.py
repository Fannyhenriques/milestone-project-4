from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

def home(request):
    return render(request, "repose/home.html")


def about(request):
    return render(request, "repose/about.html")


def treatments(request):
    return render(request, "repose/treatments.html")


def packages(request):
    return render(request, "repose/packages.html")


def membership(request):
    return render(request, "repose/membership.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "repose/register.html", {"form": form})