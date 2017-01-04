"""Tests for workshop model."""
import datetime

from api.models import Workshop

from django.test import TestCase

from freezegun import freeze_time

from model_mommy import mommy


class WorkshopTest(TestCase):
    """Test workshop methods."""

    def test_string_representation(self):
        """Test that workshop turns to string properly."""
        entry = Workshop(name="Foo Workshop")
        self.assertEqual(str(entry), 'Foo Workshop')

    @freeze_time("2017-02-01")
    def test_capacity(self):
        reservation = mommy.make(
            'api.Reservation',
            ends_at=datetime.datetime(year=2017, month=3, day=1),
            workshop_price__workshop__capacity=1,
            order__paid=False,
        )
        workshop = reservation.workshop_price.workshop
        self.assertEqual(workshop.number_of_reservations(), 1)
        self.assertEqual(workshop.has_free_capacity(), False)

    @freeze_time("2017-02-01")
    def test_capacity_after_reservation(self):
        reservation = mommy.make(
            'api.Reservation',
            ends_at=datetime.datetime(year=2017, month=1, day=1),
            workshop_price__workshop__capacity=1,
            order__paid=False,
        )
        workshop = reservation.workshop_price.workshop
        self.assertEqual(workshop.number_of_reservations(), 0)
        self.assertEqual(workshop.has_free_capacity(), True)

    @freeze_time("2017-02-01")
    def test_capacity_paid(self):
        reservation = mommy.make(
            'api.Reservation',
            ends_at=datetime.datetime(year=2017, month=1, day=1),
            workshop_price__workshop__capacity=1,
            order__paid=True,
        )
        workshop = reservation.workshop_price.workshop
        self.assertEqual(workshop.number_of_reservations(), 1)
        self.assertEqual(workshop.has_free_capacity(), False)
