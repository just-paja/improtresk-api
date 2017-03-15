"""Tests for participant model."""
from django.test import TestCase

from model_mommy import mommy


class OrderTest(TestCase):

    def setUp(self):
        workshop_price = mommy.make(
            'api.WorkshopPrice',
            workshop__name="Foo workshop",
            workshop__lectors=[mommy.make(
                'api.Lector',
                name="Foo Lector",
            )],
        )
        self.order = mommy.make(
            'api.Order',
            symvar=38212,
            price=1200,
            reservation__ends_at="2016-01-23",
            reservation__workshop_price=workshop_price,
        )

    def test_get_confirm_mail_body(self):
        self.assertEquals(
            self.order.get_mail_confirm_body(),
            """Ahoj,

Přijali jsme tvojí přihlášku. Na workshop tě však zařadíme až v \
momentě kdy bude zaplacena. Rezervujeme ti místo na workshopu do \
2016-01-23, pokud nám od tebe nepřijde platba včas, tak tvoje \
místo na workshopu nabídneme ostatním.

O zařazení na workshop a potvrzení platby ti přijde oznámení e-mailem.

Číslo účtu: 2800754192/2010
Částka k zaplacení: 1200 Kč
Variabilní symbol: 38212

Objednaný workshop: Foo workshop
Čas propadnutí rezervace: 2016-01-23

    -----

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.

Organizační tým Improtřesku 2017
http://improtresk.cz
info@improtresk.cz

--

Tato zpráva byla vyžádána v rámci placené přihlášky na Improtřesk 2017.
"""
        )
