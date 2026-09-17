from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("treatments/", views.treatments, name="treatments"),
    path("packages/", views.packages, name="packages"),
    path("membership/", views.membership, name="membership"),
]