"""Tests for reservation model."""
from django.test import TestCase

from freezegun import freeze_time

from model_mommy import mommy


class RulesTest(TestCase):
    """Test rules methods."""

    @freeze_time("2017-01-20T03:04:05")
    def test_string_representation(self):
        """Test that reservation turns to string properly."""
        rules = mommy.make(
            'Rules',
            text="foo",
            year__year="1234",
        )
        self.assertEqual(str(rules), 'Rules (2017-01-20 03:04:05+00:00) for Year 1234')
