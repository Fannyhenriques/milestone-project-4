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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        membership = None

        if user and user.is_authenticated:
            membership = getattr(user, "membership", None)

        if (
            membership
            and membership.is_active
            and membership.start_date <= timezone.localdate()
            and membership.end_date >= timezone.localdate()
        ):
            self.fields["booking_type"].choices = [
                choice
                for choice in self.fields["booking_type"].choices
                if choice[0] != "spa"
            ]

    def clean(self):
        cleaned_data = super().clean()

        booking_type = cleaned_data.get("booking_type")
        treatment = cleaned_data.get("treatment")
        package = cleaned_data.get("package")

        if booking_type == "treatment" and not treatment:
            self.add_error(
                "treatment",
                "Please select a treatment.",
            )

        if booking_type == "package" and not package:
            self.add_error(
                "package",
                "Please select a package.",
            )

        membership = None

        if self.user and self.user.is_authenticated:
            membership = getattr(self.user, "membership", None)

        if (
            booking_type == "spa"
            and membership
            and membership.is_active
            and membership.start_date <= timezone.localdate()
            and membership.end_date >= timezone.localdate()
        ):
            self.add_error(
                "booking_type",
                "Spa access is included with your membership and does not require a booking.",
            )

        return cleaned_data


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

    def __init__(self, *args, booking_data=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.booking_data = booking_data or {}
        self.user = user

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
            membership = None

            if user and user.is_authenticated:
                membership = getattr(user, "membership", None)

            if (
                membership
                and membership.is_active
                and membership.start_date <= timezone.localdate()
                and membership.end_date >= timezone.localdate()
            ):
                self.fields["number_of_guests"].choices = [
                    (1, "1"),
                ]

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
                        7,
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
            "guest_first_name",
            "guest_last_name",
            "guest_email",
        ]
        labels = {
            "guest_first_name": "First name",
            "guest_last_name": "Last name",
            "guest_email": "Email",
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields["guest_first_name"].initial = user.first_name
            self.fields["guest_last_name"].initial = user.last_name
            self.fields["guest_email"].initial = user.email

            self.fields["guest_first_name"].disabled = True
            self.fields["guest_last_name"].disabled = True
            self.fields["guest_email"].disabled = True