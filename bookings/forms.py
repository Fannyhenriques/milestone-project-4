from django import forms
from django.utils import timezone

from .models import Booking

from services.models import Package


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "booking_type",
            "treatment",
            "package",
        ]


class BookingDetailsForm(forms.ModelForm):
    number_of_guests = forms.TypedChoiceField(
        choices=[],
        coerce=int,
        label="Number of guests",
    )

    class Meta:
        model = Booking
        fields = [
            "number_of_guests",
            "booking_date",
            "booking_time",
        ]
        widgets = {
            "booking_date": forms.DateInput(attrs={"type": "date"}),
            "booking_time": forms.Select(),
        }

    def __init__(self, *args, booking_data=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["booking_date"].widget.attrs["min"] = (
            timezone.localdate().isoformat()
        )

        self.fields["booking_time"].widget.choices = []

        if not booking_data:
            return

        booking_type = booking_data.get("booking_type")

        self.fields["number_of_guests"].choices = [
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
            (6, "6"),
        ]

        if booking_type == "spa":
            self.fields["booking_time"].widget.choices = [
                ("09:00", "09:00 - 12:00"),
                ("13:00", "13:00 - 16:00"),
                ("17:00", "17:00 - 20:00"),
            ]

        elif booking_type == "treatment":
            self.fields["booking_time"].widget.choices = [
                ("09:00", "09:00"),
                ("10:00", "10:00"),
                ("11:00", "11:00"),
                ("13:00", "13:00"),
                ("14:00", "14:00"),
                ("15:00", "15:00"),
                ("16:00", "16:00"),
                ("17:00", "17:00"),
            ]

        elif booking_type == "package":
            package_id = booking_data.get("package_id")
            package = Package.objects.filter(id=package_id).first()

            if package:
                guests_per_package = package.guests_per_package

                self.fields["number_of_guests"].choices = [
                    (guests, str(guests))
                    for guests in range(
                        guests_per_package,
                        guests_per_package * 4,
                        guests_per_package,
                    )
                ]
                if package.time_period == "morning":
                    choices = [
                        ("09:00", "09:00"),
                    ]
                elif package.time_period == "afternoon":
                    choices = [
                        ("13:00", "13:00"),
                    ]
                elif package.time_period == "evening":
                    choices = [
                        ("17:00", "17:00"),
                    ]
                else:
                    choices = [
                        ("09:00", "09:00"),
                        ("13:00", "13:00"),
                        ("17:00", "17:00"),
                    ]

                self.fields["booking_time"].widget.choices = choices

    def clean_booking_date(self):
        booking_date = self.cleaned_data["booking_date"]

        if booking_date < timezone.localdate():
            raise forms.ValidationError(
                "Please select today or a future date."
            )

        return booking_date


class BookingGuestForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "guest_name",
            "guest_email",
        ]