from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "booking_type",
            "treatment",
            "package",
            "guest_name",
            "guest_email",
            "booking_date",
            "booking_time",
        ]