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
            order__participant__name="Foo participant",
        )
        workshop = reservation.workshop_price.workshop
        self.assertEqual(workshop.number_of_reservations(), 1)
        self.assertEqual(workshop.has_free_capacity(), False)

    def test_lector_names(self):
        """ Test, that Workshop.lector_names() works correctly with one lector """
        workshop = mommy.make(
            'api.Workshop',
            lectors=[
                mommy.make('api.Lector', name="Foo lector"),
            ],
        )
        self.assertEqual(workshop.lector_names(), "Foo lector")

    def test_lector_names_two(self):
        """ Test, that Workshop.lector_names() works correctly with two lectors """
        workshop = mommy.make(
            'api.Workshop',
            lectors=[
                mommy.make('api.Lector', name="Foo lector"),
                mommy.make('api.Lector', name="Bar lector"),
            ],
        )
        self.assertEqual(workshop.lector_names(), "Foo lector, Bar lector")
