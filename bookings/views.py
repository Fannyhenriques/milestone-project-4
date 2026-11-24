from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BookingRescheduleForm
from .models import Booking


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