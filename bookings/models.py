from django.conf import settings
from django.db import models

from services.models import Package, Treatment


class Booking(models.Model):
    BOOKING_TYPE_CHOICES = [
        ("spa", "Spa Access"),
        ("treatment", "Treatment"),
        ("package", "Package"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )

    booking_type = models.CharField(
        max_length=20,
        choices=BOOKING_TYPE_CHOICES,
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
    )

    treatment = models.ForeignKey(
        Treatment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    number_of_guests = models.PositiveIntegerField(default=1)
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    booking_date = models.DateField()
    booking_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def duration_minutes(self):
        if self.booking_type == "spa":
            return 180

        if self.booking_type == "treatment" and self.treatment:
            return self.treatment.duration

        if self.booking_type == "package" and self.package:
            return self.package.duration

        return 0

    def __str__(self):
        return f"{self.guest_name} - {self.booking_date}"