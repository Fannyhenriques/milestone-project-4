from django.conf import settings
from django.db import models

from services.models import Package, Treatment


class Booking(models.Model):
    BOOKING_TYPE_CHOICES = [
        ("treatment", "Treatment"),
        ("package", "Package"),
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
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    booking_date = models.DateField()
    booking_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest_name} - {self.booking_date}"