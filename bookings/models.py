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
        ("cancelled", "Cancelled"),
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

    stripe_payment_intent_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
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
    guest_first_name = models.CharField(max_length=50)
    guest_last_name = models.CharField(max_length=50)
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
        return (
            f"{self.guest_first_name} "
            f"{self.guest_last_name} - {self.booking_date}"
        )


class CancellationRecord(models.Model):
    REFUND_STATUS_CHOICES = [
        ("processing", "Processing"),
        ("pending", "Pending"),
        ("succeeded", "Succeeded"),
        ("failed", "Failed"),
    ]

    original_booking_id = models.PositiveBigIntegerField(
        unique=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cancellation_records",
    )

    booking_date = models.DateField()
    booking_time = models.TimeField()

    stripe_payment_intent_id = models.CharField(
        max_length=255,
    )

    stripe_refund_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )

    refund_status = models.CharField(
        max_length=20,
        choices=REFUND_STATUS_CHOICES,
        default="processing",
    )

    refund_amount = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    currency = models.CharField(
        max_length=3,
        default="gbp",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Cancellation for booking {self.original_booking_id}"
        )
