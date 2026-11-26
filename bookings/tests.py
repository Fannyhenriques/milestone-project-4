
from datetime import time, timedelta
from types import SimpleNamespace
from unittest.mock import Mock, patch

import stripe

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Booking, CancellationRecord


class BookingCancellationTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        self.booking = Booking.objects.create(
            user=self.user,
            booking_type="spa",
            payment_status="paid",
            number_of_guests=1,
            guest_first_name="Test",
            guest_last_name="User",
            guest_email="test@example.com",
            booking_date=timezone.localdate() + timedelta(days=7),
            booking_time=time(14, 0),
        )

        self.cancel_url = reverse(
            "cancel_booking",
            args=[self.booking.id],
        )

    def test_user_can_cancel_without_stripe_id(self):
        self.client.force_login(self.user)

        response = self.client.post(self.cancel_url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Booking.objects.filter(id=self.booking.id).exists()
        )

        cancellation = CancellationRecord.objects.get(
            original_booking_id=self.booking.id
        )

        self.assertEqual(cancellation.service_name, "Spa Access")
        self.assertEqual(cancellation.refund_status, "needs_review")

    def test_other_user_cannot_cancel_booking(self):
        other_user = get_user_model().objects.create_user(
            username="otheruser",
            password="testpassword123",
        )

        self.client.force_login(other_user)

        response = self.client.post(self.cancel_url)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Booking.objects.filter(id=self.booking.id).exists()
        )

    @patch("bookings.views.stripe.Refund.create")
    def test_stripe_failure_does_not_prevent_cancellation(
        self, mock_refund
    ):
        self.client.force_login(self.user)

        self.booking.stripe_payment_intent_id = "pi_test_failure"
        self.booking.save()

        mock_refund.side_effect = stripe.StripeError(
            "Simulated Stripe failure"
        )

        response = self.client.post(self.cancel_url)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Booking.objects.filter(id=self.booking.id).exists()
        )

        cancellation = CancellationRecord.objects.get(
            original_booking_id=self.booking.id
        )

        self.assertEqual(
            cancellation.refund_status,
            "needs_review",
        )

        mock_refund.assert_called_once()


    @patch("bookings.views.stripe.Refund.create")
    def test_successful_refund(self, mock_refund):
        self.client.force_login(self.user)

        self.booking.stripe_payment_intent_id = "pi_test_success"
        self.booking.save()

        mock_refund.return_value = SimpleNamespace(
            id="re_test_success",
            status="succeeded",
            amount=4900,
            currency="gbp",
        )

        response = self.client.post(self.cancel_url)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Booking.objects.filter(id=self.booking.id).exists()
        )

        cancellation = CancellationRecord.objects.get(
            original_booking_id=self.booking.id
        )

        self.assertEqual(cancellation.refund_status, "succeeded")
        self.assertEqual(
            cancellation.stripe_refund_id,
            "re_test_success",
        )

        mock_refund.assert_called_once()


    @patch("bookings.views.stripe.Refund.create")
    def test_pending_refund(self, mock_refund):
        self.client.force_login(self.user)

        self.booking.stripe_payment_intent_id = "pi_test_pending"
        self.booking.save()

        mock_refund.return_value = SimpleNamespace(
            id="re_test_pending",
            status="pending",
            amount=4900,
            currency="gbp",
        )

        response = self.client.post(self.cancel_url)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Booking.objects.filter(id=self.booking.id).exists()
        )

        cancellation = CancellationRecord.objects.get(
            original_booking_id=self.booking.id
        )

        self.assertEqual(cancellation.refund_status, "pending")

        mock_refund.assert_called_once()

    @patch("repose.views.stripe.Refund.retrieve")
    @patch("repose.views.stripe.Webhook.construct_event")
    def test_webhook_updates_correct_cancellation(
        self, mock_event, mock_retrieve
    ):
        cancellation = CancellationRecord.objects.create(
            original_booking_id=self.booking.id,
            user=self.user,
            booking_date=self.booking.booking_date,
            booking_time=self.booking.booking_time,
            service_name="Spa Access",
            stripe_payment_intent_id="pi_test_pending",
            stripe_refund_id="re_test_pending",
            refund_status="pending",
        )

        other_cancellation = CancellationRecord.objects.create(
            original_booking_id=self.booking.id + 1000,
            user=self.user,
            booking_date=self.booking.booking_date,
            booking_time=self.booking.booking_time,
            service_name="Another Booking",
            stripe_payment_intent_id="pi_other",
            stripe_refund_id="re_other",
            refund_status="pending",
        )

        refund_object = Mock()
        refund_object.to_dict.return_value = {
            "id": "re_test_pending",
            "payment_intent": "pi_test_pending",
            "amount": 4900,
            "currency": "gbp",
            "metadata": {"booking_id": str(self.booking.id)},
        }

        mock_event.return_value = {
            "type": "refund.updated",
            "data": {"object": refund_object},
        }

        mock_retrieve.return_value = SimpleNamespace(
            status="succeeded",
        )

        response = self.client.post(
            reverse("stripe_webhook"),
            data="{}",
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE="test_signature",
        )

        self.assertEqual(response.status_code, 200)

        cancellation.refresh_from_db()
        other_cancellation.refresh_from_db()

        self.assertEqual(cancellation.refund_status, "succeeded")
        self.assertEqual(other_cancellation.refund_status, "pending")

        mock_retrieve.assert_called_once_with("re_test_pending")

    @patch("bookings.views.stripe.Refund.create")
    def test_booking_cannot_be_refunded_twice(self, mock_refund):
        self.client.force_login(self.user)

        self.booking.stripe_payment_intent_id = "pi_test_double"
        self.booking.save()

        mock_refund.return_value = SimpleNamespace(
            id="re_test_double",
            status="pending",
            amount=4900,
            currency="gbp",
        )

        first_response = self.client.post(self.cancel_url)
        second_response = self.client.post(self.cancel_url)

        self.assertEqual(first_response.status_code, 302)
        self.assertEqual(second_response.status_code, 404)

        self.assertEqual(
            CancellationRecord.objects.filter(
                original_booking_id=self.booking.id
            ).count(),
            1,
        )

        mock_refund.assert_called_once()

    
    @patch("bookings.views.stripe.Refund.create")
    def test_refund_requires_action(self, mock_refund):
        self.client.force_login(self.user)

        self.booking.stripe_payment_intent_id = "pi_test_requires_action"
        self.booking.save()

        mock_refund.return_value = SimpleNamespace(
            id="re_test_requires_action",
            status="requires_action",
            amount=4900,
            currency="gbp",
        )

        response = self.client.post(self.cancel_url)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Booking.objects.filter(id=self.booking.id).exists()
        )

        cancellation = CancellationRecord.objects.get(
            original_booking_id=self.booking.id
        )

        self.assertEqual(
            cancellation.refund_status,
            "requires_action",
        )
        self.assertEqual(
            cancellation.stripe_refund_id,
            "re_test_requires_action",
        )

        mock_refund.assert_called_once()


class BookingRescheduleTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        self.booking = Booking.objects.create(
            user=self.user,
            booking_type="spa",
            payment_status="paid",
            number_of_guests=1,
            guest_first_name="Test",
            guest_last_name="User",
            guest_email="test@example.com",
            booking_date=timezone.localdate() + timedelta(days=7),
            booking_time=time(13, 0),
        )

        self.reschedule_url = reverse(
            "reschedule_booking",
            args=[self.booking.id],
        )

    def test_user_can_reschedule_own_booking(self):
        self.client.force_login(self.user)

        new_date = timezone.localdate() + timedelta(days=8)

        response = self.client.post(
            self.reschedule_url,
            {
                "booking_date": new_date.isoformat(),
                "booking_time": "17:00",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.booking.refresh_from_db()

        self.assertEqual(self.booking.booking_date, new_date)
        self.assertEqual(self.booking.booking_time, time(17, 0))

    def test_user_cannot_reschedule_another_users_booking(self):
        other_user = get_user_model().objects.create_user(
            username="otheruser",
            password="testpassword123",
        )

        self.client.force_login(other_user)

        response = self.client.post(
            self.reschedule_url,
            {
                "booking_date": (
                    timezone.localdate() + timedelta(days=8)
                ).isoformat(),
                "booking_time": "17:00",
            },
        )

        self.assertEqual(response.status_code, 404)

        self.booking.refresh_from_db()

        self.assertEqual(
            self.booking.booking_date,
            timezone.localdate() + timedelta(days=7),
        )
        self.assertEqual(self.booking.booking_time, time(13, 0))

    def test_cannot_reschedule_to_past_date(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.reschedule_url,
            {
                "booking_date": (
                    timezone.localdate() - timedelta(days=1)
                ).isoformat(),
                "booking_time": "17:00",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "booking_date",
            response.context["form"].errors,
        )

        self.booking.refresh_from_db()

        self.assertEqual(
            self.booking.booking_date,
            timezone.localdate() + timedelta(days=7),
        )

    def test_cannot_reschedule_to_invalid_time(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.reschedule_url,
            {
                "booking_date": (
                    timezone.localdate() + timedelta(days=8)
                ).isoformat(),
                "booking_time": "12:00",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "booking_time",
            response.context["form"].errors,
        )

        self.booking.refresh_from_db()

        self.assertEqual(self.booking.booking_time, time(13, 0))

    def test_cannot_reschedule_past_booking(self):
        self.client.force_login(self.user)

        past_date = timezone.localdate() - timedelta(days=1)
        self.booking.booking_date = past_date
        self.booking.save()

        response = self.client.post(
            self.reschedule_url,
            {
                "booking_date": (
                    timezone.localdate() + timedelta(days=8)
                ).isoformat(),
                "booking_time": "17:00",
            },
        )

        self.assertEqual(response.status_code, 404)

        self.booking.refresh_from_db()
        self.assertEqual(self.booking.booking_date, past_date)
        self.assertEqual(self.booking.booking_time, time(13, 0))

    def test_login_required_for_rescheduling(self):
        response = self.client.get(self.reschedule_url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("next=", response.url)