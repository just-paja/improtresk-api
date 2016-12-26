"""Tests for WorkshopLector model."""
from api.models import Lector, LectorRole, WorkshopLector

from django.test import TestCase


class WorkshopLectorTest(TestCase):
    """Test workshopLector methods."""

    def test_string_representation(self):
        """Test that workshop turns to string properly."""
        lector = Lector(name="Foo Lector")
        role = LectorRole(name="Foo lectorRole")
        entry = WorkshopLector(lector=lector, role=role)
        self.assertEqual(str(entry), 'Foo Lector (Foo lectorRole)')
