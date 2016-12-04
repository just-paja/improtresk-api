"""Tests for workshop model."""
from django.test import TestCase
from api.models.accomodation import Accomodation


class AccomodationTest(TestCase):
    """Test accomodation methods."""

    def test_string_representation(self):
        """Test that accomodation turns to string properly."""
        entry = Accomodation(name="Foo Accomodation")
        self.assertEqual(str(entry), 'Foo Accomodation')
