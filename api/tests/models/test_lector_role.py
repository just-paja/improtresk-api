"""Tests for lector role model."""
from api.models.lectorRole import LectorRole

from django.test import TestCase


class LectorRoleTest(TestCase):
    """Test lectorRole methods."""

    def test_string_representation(self):
        """Test that workshop turns to string properly."""
        entry = LectorRole(name="Foo LectorRole")
        self.assertEqual(str(entry), 'Foo LectorRole')
