#!/usr/bin/env python
from django.core.management.base import BaseCommand

from ...models.order import unassigned_orders


def get_order_desc(order):
    return (
        order.participant.name,
        order.symvar,
        order.reservation.workshop_price.workshop.name,
    )


class Command(BaseCommand):
    help = 'Assigns paid participants orders until available'

    def handle(self, *args, **kwargs):
        orders = unassigned_orders().order_by('created_at')
        for order in orders:
            print('Assigning %s (%s) to %s' % get_order_desc(order))
            assigned = order.try_to_assign()
            if not assigned:
                print('Failed to assign %s (%s) to %s' % get_order_desc(order))
                break
