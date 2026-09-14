from django.shortcuts import render

def home(request):
    return render(request, "repose/home.html")