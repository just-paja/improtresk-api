"""Tests for text model."""
from api_textual.models import Text

from django.test import TestCase


class TextTest(TestCase):
    """Test Text methods."""

    def test_string_representation(self):
        """Test that Text turns to string properly."""
        entry = Text(name="Foo Text")
        self.assertEqual(str(entry), 'Foo Text')
