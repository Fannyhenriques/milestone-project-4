from services.models import Treatment
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def home(request):
    return render(request, "repose/home.html")


def about(request):
    return render(request, "repose/about.html")


def treatments(request):
    treatments = Treatment.objects.filter(is_active=True)
    
    return render(
        request,
        "repose/treatments.html",
        {"treatments": treatments},
    )


def packages(request):
    return render(request, "repose/packages.html")


def membership(request):
    return render(request, "repose/membership.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("account")

    next_page = request.GET.get("next")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            if request.POST.get("next") == "membership":
                return redirect("membership")

            return redirect("account")
    else:
        form = UserCreationForm()

    return render(
        request,
        "repose/register.html",
        {
            "form": form,
            "next": next_page,
        },
    )


def booking(request):
    return render(request, "repose/booking.html")


@login_required
def account(request):
    return render(request, "repose/account.html")