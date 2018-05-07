"""Tests for orders rest endpoint."""

from django.test import TestCase

from api.codes import encrypt, decrypt


class NastyCodeTestIWillNeverDoThisAgain(TestCase):
    """
        Nasty test codes. Everything about this is temporary and feels like a
        wrong test.
    """

    def test_codes_are_two_way(self):
        for number in range(1, 10000):
            symvar = '2018%s' % number
            self.assertEqual(decrypt(encrypt(symvar)), symvar)
