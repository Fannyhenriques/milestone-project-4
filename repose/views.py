from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
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
    if request.user.is_authenticated:
        return redirect("account")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "repose/register.html", {"form": form})


def booking(request):
    return render(request, "repose/booking.html")


@login_required
def account(request):
    return render(request, "repose/account.html")