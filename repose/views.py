from django.shortcuts import render

def home(request):
    return render(request, "repose/home.html")


def about(request):
    return render(request, "repose/about.html")


def treatments(request):
    return render(request, "repose/treatments.html")


def packages(request):
    return render(request, "repose/packages.html")