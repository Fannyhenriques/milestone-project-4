from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("treatments/", views.treatments, name="treatments"),
    path("packages/", views.packages, name="packages"),
    path("membership/", views.membership, name="membership"),
    path("register/", views.register, name="register"),
    path(
    "login/",
    auth_views.LoginView.as_view(
        template_name="repose/login.html",
        redirect_authenticated_user=True,
    ),
    name="login",
),
    path("account/", views.account, name="account"),
    path("book/", views.booking, name="booking"),
    path("book/details/", views.booking_details, name="booking_details"),
    path("book/guest/", views.booking_guest, name="booking_guest"),
    path("book/review/", views.booking_review, name="booking_review"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]