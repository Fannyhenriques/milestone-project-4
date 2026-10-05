from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "booking_type",
            "treatment",
            "package",
        ]


class BookingDetailsForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "number_of_guests",
            "booking_date",
            "booking_time",
        ]
        widgets = {
            "booking_date": forms.DateInput(attrs={"type": "date"}),
            "booking_time": forms.TimeInput(attrs={"type": "time"}),
        }


class BookingGuestForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "guest_name",
            "guest_email",
        ]