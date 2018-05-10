#!/usr/bin/env python
import json

from django.core.management.base import BaseCommand

from ...models import Year, Order, Reservation


class Command(BaseCommand):
    help = 'Parses FIO bank statements'

    def handle(self, *args, **kwargs):
        year = Year.objects.get_current()
        orders = Order.objects.filter(
            year=year,
            paid=True,
            canceled=False,
        ).all()
        data = []
        for order in orders:
            food = []
            try:
                reservation = order.reservation
            except Reservation.DoesNotExist:
                continue

            meals = reservation.mealreservation_set.all()
            for meal in meals:
                food.append({
                    'date': str(meal.meal.date),
                    'food': meal.food.name if meal.food else None,
                    'id': meal.food.id if meal.food else None,
                })
            data.append({
                'id': order.participant.id,
                'participant': order.participant.name,
                'workshop': (
                    reservation.workshop_price.workshop.name
                    if reservation.workshop_price else None
                ),
                'accomodation': (
                    reservation.accomodation.name
                    if reservation.accomodation else None
                ),
                'food': food,
            })
        with open('improtresk-welcome-cards-data.json', 'w') as outfile:
            json.dump(data, outfile)
