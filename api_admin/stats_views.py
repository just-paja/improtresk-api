from api.models import (
    Food,
    Order,
    Participant,
    Reservation,
    Soup,
    Year,
)

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Sum
from django.shortcuts import render
from django.utils import timezone


@staff_member_required
def index(request):
    festivals = Year.objects.all()
    return render(
        request,
        'stats/index.html',
        {
            'festivals': festivals,
        },
    )


def update_food(mixed_food):
    for food in mixed_food:
        food.paid_reservations = (
            food
            .get_reservations_query()
            .filter(
                order__paid=True,
                order__confirmed=True,
                order__canceled=False,
            )
            .count()
        )
        food.unpaid_reservations = (
            food
            .get_reservations_query()
            .filter(
                order__paid=False,
                order__confirmed=True,
                order__canceled=False,
            )
            .count()
        )


def update_meal_reservation(meal, reservation):
    reservation.meal_reservation = (
        reservation
        .mealreservation_set
        .filter(meal=meal.pk)
        .first()
    )
    return reservation


def update_meal(meal):
    meal.unpicked_paid_reservations = (
        meal
        .get_reservations_query()
        .filter(
            order__paid=True,
            order__confirmed=True,
            order__canceled=False,
            ends_at__lte=timezone.now(),
        )
        .filter(
            Q(mealreservation__meal=meal),
            Q(mealreservation__food__isnull=True) |
            Q(mealreservation__soup__isnull=True),
        )
    )

    meal.unpicked_unpaid_reservations = (
        meal
        .get_reservations_query()
        .filter(
            order__paid=False,
            order__confirmed=True,
            order__canceled=False,
            ends_at__lte=timezone.now(),
        )
        .filter(
            Q(mealreservation__meal=meal),
            Q(mealreservation__food__isnull=True) |
            Q(mealreservation__soup__isnull=True),
        )
    )

    meal.unpicked_paid_reservations_count = (
        meal.unpicked_paid_reservations.count()
    )
    meal.unpicked_unpaid_reservations_count = (
        meal.unpicked_unpaid_reservations.count()
    )

    meal.unpicked_paid_reservations = [
        update_meal_reservation(meal, res) for res in
        meal.unpicked_paid_reservations
    ]
    meal.unpicked_unpaid_reservations = [
        update_meal_reservation(meal, res) for res in
        meal.unpicked_unpaid_reservations
    ]


@staff_member_required
def food(request, festivalId):
    festival = Year.objects.get(pk=festivalId)
    meals = festival.meals.all()
    order = []

    for meal in meals:
        soups = Soup.objects.filter(meal=meal.id).all()
        foods = Food.objects.filter(meal=meal.id).all()

        order += soups
        order += foods

        update_meal(meal)
        update_food(soups)
        update_food(foods)

    return render(
        request,
        'stats/food.html',
        {
            'festival': festival,
            'meals': meals,
            'order': order,
        },
    )


def load_food_counts(foods, location, soup=False):
    for food in foods:
        food.deliver = food.get_reservations_query().filter(
            order__paid=True,
            order__confirmed=True,
            order__canceled=False,
            workshop_price__workshop__location=location,
        ).count()
    return foods


@staff_member_required
def food_per_location(request, festivalId):
    festival = Year.objects.get(pk=festivalId)
    locations = festival.get_locations()
    meals = festival.meals.all()
    delivery = []

    for meal in meals:
        meal.delivery = []
        delivery.append(meal)

        for location in locations:
            meal.delivery.append(location)
            location.delivery = []
            soups = Soup.objects.filter(meal=meal.id).all()
            foods = Food.objects.filter(meal=meal.id).all()

            location.delivery += load_food_counts(soups, location)
            location.delivery += load_food_counts(foods, location, True)

    return render(
        request,
        'stats/food_per_location.html',
        {
            'festival': festival,
            'delivery': delivery,
        },
    )


@staff_member_required
def workshops(request, festivalId):
    festival = Year.objects.get(pk=festivalId)
    workshops = festival.get_workshops()

    for workshop in workshops:
        workshop.participant_count = workshop.participant_set.count()
        workshop.participant_list = workshop.participant_set.all()

    return render(
        request,
        'stats/workshops.html',
        {
            'festival': festival,
            'workshops': workshops,
        },
    )


@staff_member_required
def accounting(request, festivalId):
    participants = Participant.objects\
        .filter(assigned_workshop__isnull=False)\
        .order_by('name')\
        .all()
    data = []

    for participant in participants:
        order = get_participant_order(participant)

        if order:
            data.append({
                'name': participant.name,
                'email': participant.email,
                'address': participant.address,
                'cash_expected': order.price,
            })

    return render(
        request,
        'stats/accounting.html',
        {
            'data': data,
        },
    )


def get_participant_order(participant):
    return Order.objects.filter(
        participant=participant,
        canceled=False,
        confirmed=True,
        paid=True,
    ).first()


def get_participant_reservation(order):
    if order:
        return Reservation.objects.filter(
            order=order,
        ).first()
    return None


@staff_member_required
def participant_list(request, festivalId):
    participants = Participant.objects\
        .filter(assigned_workshop__isnull=False)\
        .order_by('name')\
        .all()
    data = []

    for participant in participants:
        order = get_participant_order(participant)
        reservation = get_participant_reservation(order)
        payment_sum = 0
        if order.payments.count() > 0:
            payment_sum = order.payments.aggregate(paid=Sum('amount')).get('paid')
        if order and reservation:
            accomodation = reservation.accomodation
            meal_reservations = reservation.mealreservation_set.all()

            data.append({
                'name': participant.name,
                'email': participant.email,
                'workshop': participant.assigned_workshop.name,
                'accomodation': accomodation.name,
                'meals': meal_reservations,
                'cash_expected': order.price,
                'cash_received': payment_sum,
            })

    return render(
        request,
        'stats/participant_list.html',
        {
            'data': data,
        },
    )
