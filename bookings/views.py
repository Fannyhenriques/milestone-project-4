import logging

import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

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
        if not booking.stripe_payment_intent_id:
            return render(
                request,
                "repose/booking_cancel_confirm.html",
                {
                    "booking": booking,
                    "error_message": (
                        "This booking cannot be refunded automatically. "
                        "Please contact us for assistance."
                    ),
                },
            )

        cancellation, created = CancellationRecord.objects.get_or_create(
            original_booking_id=booking.id,
            defaults={
                "user": request.user,
                "booking_date": booking.booking_date,
                "booking_time": booking.booking_time,
                "stripe_payment_intent_id": (
                    booking.stripe_payment_intent_id
                ),
            },
        )

        if not created:
            if (
                cancellation.stripe_refund_id
                and cancellation.refund_status == "succeeded"
            ):
                booking.delete()
                request.session["booking_cancellation_success"] = True
                return redirect("cancellation_success")

            return render(
                request,
                "repose/booking_cancel_confirm.html",
                {
                    "booking": booking,
                    "error_message": (
                        "A refund request is already being reviewed. "
                        "Please contact us for assistance."
                    ),
                },
            )

        try:
            refund = stripe.Refund.create(
                payment_intent=booking.stripe_payment_intent_id,
                reason="requested_by_customer",
                metadata={"booking_id": str(booking.id)},
                idempotency_key=f"repose-booking-refund-{booking.id}",
            )

        except stripe.StripeError:
            logger.exception(
                "Stripe refund request could not be confirmed "
                "for booking %s",
                booking.id,
            )

            return render(
                request,
                "repose/booking_cancel_confirm.html",
                {
                    "booking": booking,
                    "error_message": (
                        "We could not confirm the refund status. "
                        "Your booking remains active in our system. "
                        "Please contact us for assistance."
                    ),
                },
            )

        cancellation.stripe_refund_id = refund.id
        cancellation.refund_amount = refund.amount
        cancellation.currency = refund.currency

        if refund.status in (
            "pending",
            "requires_action",
            "succeeded",
            "failed",
            "canceled",
        ):
            cancellation.refund_status = refund.status
        else:
            cancellation.refund_status = "processing"

        cancellation.save()

        if refund.status == "succeeded":
            booking.delete()
            request.session["booking_cancellation_success"] = True
            return redirect("cancellation_success")

        if refund.status == "pending":
            return render(
                request,
                "repose/booking_cancel_confirm.html",
                {
                    "booking": booking,
                    "error_message": (
                        "Your refund request is being processed. "
                        "Your booking remains visible until the "
                        "refund has been confirmed."
                    ),
                },
            )

        return render(
            request,
            "repose/booking_cancel_confirm.html",
            {
                "booking": booking,
                "error_message": (
                    "The refund could not be completed automatically. "
                    "Your booking remains active. "
                    "Please contact us for assistance."
                ),
            },
        )

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

    return render(
        request,
        "repose/booking_success.html",
        {"is_cancellation": True},
    )
