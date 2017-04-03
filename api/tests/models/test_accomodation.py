"""Tests for workshop model."""

from api.models.accomodation import Accomodation

from dateutil.parser import parse

from django.test import TestCase

from freezegun import freeze_time

from model_mommy import mommy


class AccomodationTest(TestCase):
    """Test accomodation methods."""

    def test_string_representation(self):
        """Test that accomodation turns to string properly."""
        entry = Accomodation(name="Foo Accomodation")
        self.assertEqual(str(entry), 'Foo Accomodation')

    @freeze_time("2017-02-01T00:00:00Z")
    def test_capacity(self):
        reservation = mommy.make(
            'api.Reservation',
            ends_at=parse('2017-03-01T00:00:00Z'),
            accomodation__capacity=1,
            order__paid=True,
        )
        reservation.order.paid = True
        reservation.order.save()
        accomodation = reservation.accomodation
        self.assertEqual(accomodation.number_of_reservations(), 1)
        self.assertEqual(accomodation.available_capacity(), 0)
        self.assertEqual(accomodation.has_free_capacity(), False)

    @freeze_time("2017-02-01T00:00:00Z")
    def test_capacity_after_reservation(self):
        reservation = mommy.make(
            'api.Reservation',
            ends_at=parse('2017-02-01T00:00:00Z'),
            accomodation__capacity=1,
        )
        accomodation = reservation.accomodation
        self.assertEqual(accomodation.number_of_reservations(), 0)
        self.assertEqual(accomodation.available_capacity(), 1)
        self.assertEqual(accomodation.has_free_capacity(), True)

    @freeze_time("2017-02-01T00:00:00Z")
    def test_capacity_paid(self):
        reservation = mommy.make(
            'api.Reservation',
            ends_at=parse('2017-02-01T00:00:00Z'),
            accomodation__capacity=1,
            order__participant__name="Foo participant",
        )
        reservation.order.paid = True
        reservation.order.save()
        accomodation = reservation.accomodation
        self.assertEqual(accomodation.number_of_reservations(), 1)
        self.assertEqual(accomodation.available_capacity(), 0)
        self.assertEqual(accomodation.has_free_capacity(), False)
