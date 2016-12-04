"""Tests for workshop model."""
from django.test import TestCase
from api.models.workshop import Workshop


class WorkshopTest(TestCase):
    """Test workshop methods."""

    def test_string_representation(self):
        """Test that workshop turns to string properly."""
        entry = Workshop(name="Foo Workshop")
        self.assertEqual(str(entry), 'Foo Workshop')
