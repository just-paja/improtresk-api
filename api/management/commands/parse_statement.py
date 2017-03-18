#!/usr/bin/env python
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from fiobank import FioBank

from ...models import Order, Payment


class Command(BaseCommand):
    help = 'Parses FIO bank statements'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days-back',
            default=7,
            type=int,
            nargs="?",
            help='Days back, for which will be the statement fetched',
        )

    def handle(self, *args, **kwargs):
        client = FioBank(token=settings.FIO_TOKEN)
        gen = client.period(
            datetime.datetime.now() - datetime.timedelta(days=kwargs['days_back']),
            datetime.datetime.now(),
        )
        for payment in gen:
            if payment['amount'] >= 0:
                variable_symbol = payment['variable_symbol']
                try:
                    order = Order.objects.get(symvar=variable_symbol)
                except Order.DoesNotExist:
                    order = None
                new_payment, created = Payment.objects.get_or_create(
                    ident=payment['transaction_id'],
                    defaults={
                        'message': payment['recipient_message'],
                        'symspc': payment['specific_symbol'],
                        'symvar': variable_symbol,
                        'currency': payment['currency'],
                        'amount': payment['amount'],
                        'received_at': payment['date'],
                        'user_identification': payment['user_identification'],
                        'bank': payment['bank_name'],
                        'symcon': payment['constant_symbol'],
                        'sender': payment['account_number_full'],
                        'status': 'paid',
                        'order': order,
                    },
                )
                if created and order:
                        order.update_paid_status()
