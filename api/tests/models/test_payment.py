"""Tests for reservation model."""

from django.test import TestCase
from model_mommy import mommy


class PaymentTest(TestCase):
    """Test Payment methods."""

    def test_string_representation(self):
        """Test that reservation turns to string properly."""
        payment = mommy.make(
            'Payment',
            received_at='2017-01-20T03:04:05Z',
        )
        self.assertEqual(str(payment), 'Payment from 2017-01-20T03:04:05Z')
