from decimal import Decimal
from datetime import date, time, datetime, timedelta

import stripe

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from bookings.forms import BookingForm, BookingDetailsForm, BookingGuestForm
from bookings.models import Booking
from services.models import Package, Treatment


stripe.api_key = settings.STRIPE_SECRET_KEY


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
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            if request.POST.get("next") == "membership":
                return redirect("membership")

            return redirect("account")
    else:
        form = RegistrationForm()

    return render(
        request,
        "repose/register.html",
        {
            "form": form,
            "next": next_page,
        },
    )


def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            treatment = form.cleaned_data["treatment"]
            package = form.cleaned_data["package"]

            request.session["booking_step_one"] = {
                "booking_type": form.cleaned_data["booking_type"],
                "treatment_id": treatment.id if treatment else None,
                "package_id": package.id if package else None,
            }

            return redirect("booking_details")
    else:
        form = BookingForm()

    return render(
        request,
        "repose/booking.html",
        {"form": form},
    )


def booking_details(request):
    if "booking_step_one" not in request.session:
        return redirect("booking")

    booking_data = request.session["booking_step_one"]

    if request.method == "POST":
        form = BookingDetailsForm(
            request.POST,
            booking_data=booking_data,
            user=request.user,
        )

        if form.is_valid():
            request.session["booking_step_two"] = {
                "number_of_guests": form.cleaned_data["number_of_guests"],
                "booking_date": form.cleaned_data["booking_date"].isoformat(),
                "booking_time": form.cleaned_data["booking_time"].isoformat(),
            }

            return redirect("booking_guest")

    else:
        form = BookingDetailsForm(
            booking_data=booking_data,
            user=request.user,
        )

    return render(
        request,
        "repose/booking_details.html",
        {"form": form},
    )


def booking_guest(request):
    if "booking_step_two" not in request.session:
        return redirect("booking_details")

    if request.method == "POST":
        form = BookingGuestForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            request.session["booking_step_three"] = {
                "guest_first_name": form.cleaned_data["guest_first_name"],
                "guest_last_name": form.cleaned_data["guest_last_name"],
                "guest_email": form.cleaned_data["guest_email"],
            }

            return redirect("booking_review")
    else:
        form = BookingGuestForm(
            user=request.user,
        )

    return render(
        request,
        "repose/booking_guest.html",
        {"form": form},
    )


def booking_review(request):
    if "booking_step_three" not in request.session:
        return redirect("booking_guest")

    step_one = request.session["booking_step_one"]
    step_two = request.session["booking_step_two"]
    step_three = request.session["booking_step_three"]

    treatment = None
    package = None

    if step_one["treatment_id"]:
        treatment = Treatment.objects.get(id=step_one["treatment_id"])

    if step_one["package_id"]:
        package = Package.objects.get(id=step_one["package_id"])

    start_time = time.fromisoformat(step_two["booking_time"])

    if step_one["booking_type"] == "spa":
        duration = 180
    elif step_one["booking_type"] == "treatment" and treatment:
        duration = treatment.duration
    elif step_one["booking_type"] == "package" and package:
        duration = package.duration
    else:
        duration = 0

    start_datetime = datetime.combine(date.today(), start_time)
    end_datetime = start_datetime + timedelta(minutes=duration)

    booking_time_display = (
        f"{start_datetime.strftime('%H:%M')} - "
        f"{end_datetime.strftime('%H:%M')}"
    )

    booking_type = step_one["booking_type"]
    member_discount = False
    original_unit_price = None

    if booking_type == "treatment":
        unit_price = treatment.price
        quantity = step_two["number_of_guests"]
        item_name = treatment.name

        membership = None

        if request.user.is_authenticated:
            membership = getattr(request.user, "membership", None)

        if (
            membership
            and membership.is_active
            and membership.start_date <= timezone.localdate()
            and membership.end_date >= timezone.localdate()
        ):
            original_unit_price = unit_price
            unit_price = (
                unit_price * Decimal("0.85")
            ).quantize(Decimal("0.01"))
            member_discount = True

    elif booking_type == "package":
        unit_price = package.price
        quantity = (
            step_two["number_of_guests"]
            // package.guests_per_package
        )
        item_name = package.name

    else:
        unit_price = Decimal("49.00")
        quantity = step_two["number_of_guests"]
        item_name = "Spa Access"

    total_price = unit_price * quantity

    if request.method == "POST":
        booking = None
        pending_booking_id = request.session.get("pending_booking_id")

        if pending_booking_id:
            booking = Booking.objects.filter(
                id=pending_booking_id,
                payment_status="pending",
            ).first()

        if not booking:
            booking = Booking.objects.create(
                user=request.user if request.user.is_authenticated else None,
                booking_type=step_one["booking_type"],
                treatment=treatment,
                package=package,
                number_of_guests=step_two["number_of_guests"],
                booking_date=date.fromisoformat(step_two["booking_date"]),
                booking_time=time.fromisoformat(step_two["booking_time"]),
                guest_first_name=step_three["guest_first_name"],
                guest_last_name=step_three["guest_last_name"],
                guest_email=step_three["guest_email"],
                payment_status="pending",
            )

            request.session["pending_booking_id"] = booking.id

        checkout_session = stripe.checkout.Session.create(
            mode="payment",
            client_reference_id=str(booking.id),
            customer_email=booking.guest_email,
            line_items=[
                {
                    "price_data": {
                        "currency": "gbp",
                        "product_data": {
                            "name": item_name,
                        },
                        "unit_amount": int(unit_price * 100),
                    },
                    "quantity": quantity,
                }
            ],
            success_url=(
                request.build_absolute_uri("/book/success/")
                + "?session_id={CHECKOUT_SESSION_ID}"
            ),
            cancel_url=request.build_absolute_uri(
                "/book/cancelled/"
            ),
        )

        return redirect(checkout_session.url, code=303)

    context = {
        "booking_type": step_one["booking_type"],
        "treatment": treatment,
        "package": package,
        "number_of_guests": step_two["number_of_guests"],
        "booking_date": step_two["booking_date"],
        "booking_time": step_two["booking_time"],
        "guest_first_name": step_three["guest_first_name"],
        "guest_last_name": step_three["guest_last_name"],
        "guest_email": step_three["guest_email"],
        "booking_time_display": booking_time_display,
        "unit_price": unit_price,
        "original_unit_price": original_unit_price,
        "quantity": quantity,
        "total_price": total_price,
        "member_discount": member_discount,
    }

    return render(
        request,
        "repose/booking_review.html",
        context,
    )


@login_required
def account(request):
    membership = getattr(request.user, "membership", None)

    return render(
        request,
        "repose/account.html",
        {"membership": membership},
    )


def booking_success(request):
    session_id = request.GET.get("session_id")

    if session_id:
        checkout_session = stripe.checkout.Session.retrieve(session_id)

        if checkout_session.payment_status == "paid":
            booking_id = checkout_session.client_reference_id

            booking = Booking.objects.filter(id=booking_id).first()

            if booking:
                booking.payment_status = "paid"
                booking.save(update_fields=["payment_status"])

    return render(
        request,
        "repose/booking_success.html",
    )


def booking_cancelled(request):
    booking_id = request.session.get("pending_booking_id")

    if booking_id:
        booking = Booking.objects.filter(
            id=booking_id,
            payment_status="pending",
        ).first()

        if booking:
            booking.payment_status = "cancelled"
            booking.save(update_fields=["payment_status"])

        request.session.pop("pending_booking_id", None)

    return render(
        request,
        "repose/booking_cancelled.html",
    )


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    signature = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        checkout_session = event["data"]["object"]

        if checkout_session["payment_status"] == "paid":
            booking_id = checkout_session.get("client_reference_id")

            booking = Booking.objects.filter(id=booking_id).first()

            if booking:
                booking.payment_status = "paid"
                booking.save(update_fields=["payment_status"])

    elif event["type"] == "checkout.session.expired":
        checkout_session = event["data"]["object"]
        booking_id = checkout_session.get("client_reference_id")

        booking = Booking.objects.filter(
            id=booking_id,
            payment_status="pending",
        ).first()

        if booking:
            booking.payment_status = "cancelled"
            booking.save(update_fields=["payment_status"])

    return HttpResponse(status=200)