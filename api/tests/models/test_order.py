"""Tests for participant model."""

from datetime import datetime

from django.core import mail
from django.test import TestCase

from model_mommy import mommy


class OrderConfirmTest(TestCase):

    def setUp(self):
        self.maxDiff = 60000
        workshop_price = mommy.make(
            'api.WorkshopPrice',
            workshop__name="Foo workshop",
            workshop__lectors=[
                mommy.make(
                    'api.Lector',
                    name="Foo Lector",
                ),
            ],
        )
        reservation = mommy.make(
            'api.Reservation',
            ends_at=datetime.strptime(
                '2017-03-12T17:30:15',
                '%Y-%m-%dT%H:%M:%S',
            ),
            workshop_price=workshop_price,
        )
        self.order = mommy.make(
            'api.Order',
            symvar=38212,
            price=1200,
            participant__email="foo@bar.com",
            reservation=reservation,
        )

    def test_mail_confirm(self):
        mail.outbox = []
        self.order.mail_confirm()
        self.assertEquals(len(mail.outbox), 1)
        sent = mail.outbox.pop()
        self.assertEquals(sent.to, ['foo@bar.com'])
        self.assertEquals(
            sent.body,
            """Ahoj,

Přijali jsme tvojí přihlášku. Na workshop tě však zařadíme až v \
momentě kdy bude zaplacena. Rezervujeme ti místo na workshopu do \
12. 3. 2017 17:30:15, pokud nám od tebe nepřijde platba včas, tak tvoje \
místo na workshopu nabídneme ostatním.

O zařazení na workshop a potvrzení platby ti přijde oznámení e-mailem.

Detaily platby:
Číslo účtu: 2800754192/2010
Částka k zaplacení: 1200 Kč
Variabilní symbol: 38212

Objednaný workshop: Foo workshop
Čas propadnutí rezervace: 12. 3. 2017 17:30:15

    -----

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.

Organizační tým Improtřesku
http://improtresk.cz
info@improtresk.cz

--

Tato zpráva byla vyžádána v rámci placené přihlášky na Improtřesk 2017.
""",
        )


class OrderUpdateTest(TestCase):

    def setUp(self):
        self.maxDiff = 60000
        workshop_price = mommy.make(
            'api.WorkshopPrice',
            workshop__name="Foo workshop",
            workshop__lectors=[
                mommy.make(
                    'api.Lector',
                    name="Foo Lector",
                ),
            ],
        )
        payment = mommy.make(
            'api.Payment',
            amount=1000,
            symvar=38212,
            status='paid',
            sender="3216354",
            bank="2010",
            received_at='2017-03-01T17:30:15',
        )
        payment.created_at = '2017-03-12T17:30:15'
        reservation = mommy.make(
            'api.Reservation',
            ends_at="2016-01-23",
            workshop_price=workshop_price,
        )
        self.order = mommy.make(
            'api.Order',
            symvar=38212,
            price=1434,
            participant__email="foo@bar.com",
            payments=[payment],
            reservation=reservation,
        )

    def test_mail_update(self):
        mail.outbox = []
        self.order.mail_update()
        self.assertEquals(len(mail.outbox), 1)
        sent = mail.outbox.pop()
        self.assertEquals(sent.to, ['foo@bar.com'])
        self.assertEquals(
            sent.body,
            """Ahoj,

posíláme ti aktualizaci tvojí přihlášky na Improtřesk 2017.

Přihláška stále není zaplacena, chybí nám od tebe 434 Kč. \
Pošli je prosím na náš účet bankovním převodem.

Workshop: Foo workshop
Číslo účtu: 2800754192/2010
Částka k zaplacení: 434 Kč
Variabilní symbol: 38212

Celkem zaplaceno: 1000 Kč

Spárované platby:

    Částka: 1000 Kč
    Odesláno z účtu: 3216354/2010
    Variabilní symbol: 38212
    Přijato bankou: 1. 3. 2017 17:30:15
    Zpracováno: 12. 3. 2017 17:30:15

    -----

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.

Organizační tým Improtřesku
http://improtresk.cz
info@improtresk.cz

--

Tato zpráva byla vyžádána v rámci placené přihlášky na Improtřesk 2017.
""",
        )


class OrderPaidTest(TestCase):

    def setUp(self):
        self.maxDiff = 60000
        workshop_price = mommy.make(
            'api.WorkshopPrice',
            workshop__name="Foo workshop",
            workshop__lectors=[
                mommy.make(
                    'api.Lector',
                    name="Foo Lector",
                ),
            ],
        )
        payment1 = mommy.make(
            'api.Payment',
            ident="a6s85",
            amount=1000,
            symvar=38212,
            status='paid',
            sender="3216354",
            bank="2010",
            received_at='2017-03-01T17:30:15',
        )
        payment2 = mommy.make(
            'api.Payment',
            ident="x123",
            amount=434,
            symvar=38212,
            status='paid',
            sender="3216354",
            bank="2010",
            received_at='2017-03-01T19:30:15',
        )
        payment1.created_at = '2017-03-12T17:30:15'
        payment2.created_at = '2017-03-12T19:30:15'
        reservation = mommy.make(
            'api.Reservation',
            ends_at="2016-01-23",
            workshop_price=workshop_price,
        )
        self.order = mommy.make(
            'api.Order',
            symvar=38212,
            price=1434,
            participant__email="foo@bar.com",
            payments=[payment1, payment2],
            reservation=reservation,
        )

    def test_mail_paid(self):
        mail.outbox = []
        self.order.mail_paid()
        self.assertEquals(len(mail.outbox), 1)
        sent = mail.outbox.pop()
        self.assertEquals(sent.to, ['foo@bar.com'])
        self.assertEquals(
            sent.body,
            """Hurá!

Tvoje přihláška je zaplacena. V tento okamžik jsi byl(a) zařazen(a) \
do fronty na workshop podle tvých preferencí. Zařazování na workshopy \
probíhá částečně manuálně a částečně automaticky - někde u počítače sedí \
člověk, který potvrzuje kdo kam půjde podle toho kdo dřív zaplatil. \
Může to tedy chvíli trvat. Jakmile tě zařadíme, okamžitě se ti ozveme.

Workshop: Foo workshop
Celkem zaplaceno: 1434 Kč

Spárované platby:

    Částka: 1000 Kč
    Odesláno z účtu: 3216354/2010
    Variabilní symbol: 38212
    Přijato bankou: 1. 3. 2017 17:30:15
    Zpracováno: 12. 3. 2017 17:30:15

    Částka: 434 Kč
    Odesláno z účtu: 3216354/2010
    Variabilní symbol: 38212
    Přijato bankou: 1. 3. 2017 19:30:15
    Zpracováno: 12. 3. 2017 19:30:15

    -----

Kdyby došlo k jakékoliv nesrovnalosti, neváhej nás prosím okamžitě kontaktovat.

Organizační tým Improtřesku
http://improtresk.cz
info@improtresk.cz

--

Tato zpráva byla vyžádána v rámci placené přihlášky na Improtřesk 2017.
""",
        )
