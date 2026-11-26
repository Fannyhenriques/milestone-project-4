import logging

import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db import transaction

from .forms import BookingRescheduleForm
from .models import Booking, CancellationRecord

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def reschedule_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        payment_status="paid",
    )

    today = timezone.localdate()

    if (
        booking.booking_date < today
        or (
            booking.booking_date == today
            and booking.booking_time <= timezone.localtime().time()
        )
    ):
        raise Http404("This booking can no longer be rescheduled.")

    if request.method == "POST":
        form = BookingRescheduleForm(
            request.POST,
            instance=booking,
        )

        if form.is_valid():
            form.save()
            return redirect("account")

    else:
        form = BookingRescheduleForm(instance=booking)

    return render(
        request,
        "repose/booking_details.html",
        {
            "form": form,
            "booking": booking,
            "is_rescheduling": True,
        },
    )


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        payment_status="paid",
    )

    today = timezone.localdate()

    if (
        booking.booking_date < today
        or (
            booking.booking_date == today
            and booking.booking_time <= timezone.localtime().time()
        )
    ):
        raise Http404("This booking can no longer be cancelled.")

    if request.method == "POST":
        with transaction.atomic():
            booking = get_object_or_404(
                Booking.objects.select_for_update(),
                id=booking_id,
                user=request.user,
                payment_status="paid",
            )

            today = timezone.localdate()

            if (
                booking.booking_date < today
                or (
                    booking.booking_date == today
                    and booking.booking_time <= timezone.localtime().time()
                )
            ):
                raise Http404("This booking can no longer be cancelled.")

            if booking.booking_type == "spa":
                service_name = "Spa Access"
            elif booking.treatment:
                service_name = booking.treatment.name
            elif booking.package:
                service_name = booking.package.name
            else:
                service_name = "Booking"

            cancellation, created = CancellationRecord.objects.get_or_create(
                original_booking_id=booking.id,
                defaults={
                    "user": request.user,
                    "booking_date": booking.booking_date,
                    "booking_time": booking.booking_time,
                    "service_name": service_name,
                    "stripe_payment_intent_id": (
                        booking.stripe_payment_intent_id
                    ),
                    "refund_status": "needs_review",
                },
            )

            booking.delete()

        if created and cancellation.stripe_payment_intent_id:
            try:
                refund = stripe.Refund.create(
                    payment_intent=cancellation.stripe_payment_intent_id,
                    reason="requested_by_customer",
                    metadata={
                        "booking_id": str(cancellation.original_booking_id)
                    },
                    idempotency_key=(
                        f"repose-booking-refund-"
                        f"{cancellation.original_booking_id}"
                    ),
                )

            except stripe.StripeError:
                logger.exception(
                    "Stripe refund could not be confirmed "
                    "for booking %s",
                    cancellation.original_booking_id,
                )

            else:
                refund_status = (
                    refund.status
                    if refund.status in (
                        "pending",
                        "requires_action",
                        "succeeded",
                        "failed",
                        "canceled",
                    )
                    else "needs_review"
                )

                CancellationRecord.objects.filter(
                    pk=cancellation.pk,
                    refund_status="needs_review",
                ).update(
                    stripe_refund_id=refund.id,
                    refund_amount=refund.amount,
                    currency=refund.currency,
                    refund_status=refund_status,
                    updated_at=timezone.now(),
                )

        cancellation.refresh_from_db()

        request.session["booking_cancellation_success"] = True
        request.session["cancellation_refund_status"] = (
            cancellation.refund_status
        )

        return redirect("cancellation_success")
    
    return render(
        request,
        "repose/booking_cancel_confirm.html",
        {"booking": booking},
    )


@login_required
def cancellation_success(request):
    if not request.session.pop(
        "booking_cancellation_success", False
    ):
        return redirect("account")

    refund_status = request.session.pop(
        "cancellation_refund_status",
        "needs_review",
    )

    return render(
        request,
        "repose/booking_success.html",
        {
            "is_cancellation": True,
            "refund_status": refund_status,
        },
    )