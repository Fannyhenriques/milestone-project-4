from services.models import Package, Treatment
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def home(request):
    return render(request, "repose/home.html")


def about(request):
    return render(request, "repose/about.html")


def treatments(request):
    active_treatments = Treatment.objects.filter(is_active=True)

    context = {
        "massages": active_treatments.filter(category="massage"),
        "body_treatments": active_treatments.filter(category="body"),
        "facials": active_treatments.filter(category="facial"),
    }

    return render(
        request,
        "repose/treatments.html",
        context,
    )


def packages(request):
    packages = Package.objects.filter(is_active=True)

    return render(
        request, 
        "repose/packages.html",
        {"packages": packages}
    )


def membership(request):
    membership = None

    if request.user.is_authenticated:
        membership = getattr(request.user, "membership", None)

    return render(
        request,
        "repose/membership.html",
        {"membership": membership},
    )


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
    membership = getattr(request.user, "membership", None)

    return render(
        request,
        "repose/account.html",
        {"membership": membership},
    )
