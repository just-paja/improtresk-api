"""Tests for participant model."""
from django.test import TestCase

from model_mommy import mommy


class OrderTest(TestCase):

    def test_get_confirm_mail_body(self):
        order = mommy.make(
            'api.Order',
            symvar=38212,
            price=1200,
            reservation__endsAt="2016-01-23",
            reservation__workshop={
                mommy.make(
                    'api.Workshop',
                    name="Foo workshop",
                    lectors=[
                        mommy.make(
                            'api.WorkshopLector',
                            lector=mommy.make(
                                'api.Lector',
                                name="Foo Lector",
                            ),
                        ),
                    ),
                ),
            },
        )

        self.assertEquals(
            order.get_mail_confirm_body(),
            'Prev workshop: Foo lector: Foo workshop, '
            'Current workshop: Foo lector: Foo workshop, '
            'Workshop preferences foo\n'
            'Organizační tým Improtřesku 2017\n'
            'http://improtresk.cz\n'
            'info@improtresk.cz\n'
            '\n'
            '--\n'
            '\n'
            'Tato zpráva byla vyžádána v rámci placené přihlášky na Improtřesk 2017.\n',
        )
