"""Tests for participant model."""

from dateutil.parser import parse
from django.core import mail
from django.test import TestCase
from model_mommy import mommy


class OrderConfirmTest(TestCase):

    def setUp(self):
        self.maxDiff = 600000
        lector = mommy.make(
            'api.Lector',
            name="Foo Lector",
        )
        workshop_price = mommy.make(
            'api.WorkshopPrice',
            workshop__name="Foo Workshop",
            workshop__lectors=[
                lector,
            ],
        )
        reservation = mommy.make(
            'api.Reservation',
            ends_at=parse('2017-03-12T17:30:15Z'),
            workshop_price=workshop_price,
        )
        self.order = mommy.make(
            'api.Order',
            symvar=38212,
            price=1200,
            participant__email="foo@bar.com",
            reservation=reservation,
        )
        mail.outbox = []

    def test_mail_confirm_is_sent_to_participant(self):
        self.order.mail_confirm()
        self.assertEquals(mail.outbox.pop().to, ['foo@bar.com'])

    def test_mail_confirm_contains_workshop_name(self):
        self.order.mail_confirm()
        self.assertIn('Foo Workshop', mail.outbox.pop().body)

    def test_mail_confirm_contains_amount_to_pay_in_crowns(self):
        self.order.mail_confirm()
        self.assertIn('1200 Kč', mail.outbox.pop().body)

    def test_mail_confirm_contains_variable_symbol(self):
        self.order.mail_confirm()
        self.assertIn('38212', mail.outbox.pop().body)

    def test_mail_confirm_contains_account_number(self):
        self.order.mail_confirm()
        self.assertIn('2800754192/2010', mail.outbox.pop().body)

    def test_mail_confirm_contains_reservation_end_time(self):
        self.order.mail_confirm()
        self.assertIn('12. 3. 2017 17:30', mail.outbox.pop().body)


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
            received_at='2017-03-01T17:30:15Z',
        )
        payment.created_at = '2017-03-12T17:30:15Z'
        reservation = mommy.make(
            'api.Reservation',
            ends_at='2016-01-23T00:00:00Z',
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
        mail.outbox = []

    def test_mail_update_sent_to_participant(self):
        self.order.mail_update()
        self.assertEquals(mail.outbox.pop().to, ['foo@bar.com'])

    def test_mail_update_contains_missing_amount(self):
        self.order.mail_update()
        self.assertIn('434 Kč', mail.outbox.pop().body)

    def test_mail_update_contains_paid_amount(self):
        self.order.mail_update()
        self.assertIn('1000 Kč', mail.outbox.pop().body)

    def test_mail_update_contains_variable_symbol(self):
        self.order.mail_update()
        self.assertIn('38212', mail.outbox.pop().body)

    def test_mail_confirm_contains_account_number(self):
        self.order.mail_update()
        self.assertIn('2800754192/2010', mail.outbox.pop().body)


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
            received_at='2017-03-01T17:30:15Z',
        )
        payment2 = mommy.make(
            'api.Payment',
            ident="x123",
            amount=434,
            symvar=38212,
            status='paid',
            sender="3216354",
            bank="2010",
            received_at='2017-03-01T19:30:15Z',
        )
        payment1.created_at = '2017-03-12T17:30:15Z'
        payment2.created_at = '2017-03-12T19:30:15Z'
        reservation = mommy.make(
            'api.Reservation',
            ends_at="2016-01-23T00:00:00Z",
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
        mail.outbox = []

    def test_mail_paid_sent_to_participant(self):
        self.order.mail_paid()
        self.assertEquals(mail.outbox.pop().to, ['foo@bar.com'])

    def test_mail_update_contains_total_payment_amount(self):
        self.order.mail_paid()
        self.assertIn('1434 Kč', mail.outbox.pop().body)

    def test_mail_update_contains_first_payment_amount(self):
        self.order.mail_paid()
        self.assertIn('1000 Kč', mail.outbox.pop().body)

    def test_mail_update_contains_second_payment_amount(self):
        self.order.mail_paid()
        self.assertIn('434 Kč', mail.outbox.pop().body)
