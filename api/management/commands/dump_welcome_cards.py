#!/usr/bin/env python
import json

from django.core.management.base import BaseCommand

from ...models import Year, Order


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
            if order.reservation:
                meals = order.reservation.mealreservation_set.all()
                for meal in meals:
                    food.append({
                        'date': str(meal.meal.date),
                        'food': meal.food.name if meal.food else None,
                    })
                data.append({
                    'id': order.participant.id,
                    'participant': order.participant.name,
                    'workshop': (
                        order.reservation.workshop_price.workshop.name
                        if order.reservation.workshop_price else None
                    ),
                    'accomodation': (
                        order.reservation.accomodation.name
                        if order.reservation.accomodation else None
                    ),
                    'food': food,
                })
        with open('improtresk-welcome-cards-data.json', 'w') as outfile:
            json.dump(data, outfile)
