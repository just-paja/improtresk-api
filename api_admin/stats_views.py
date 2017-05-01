from api.models import Food, Soup, Year

from django.shortcuts import render


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


def update_meal(meal):
    meal.unpicked_paid_reservations = (
        meal
        .get_reservations_query()
        .filter(
            order__paid=True,
            order__confirmed=True,
            order__canceled=False,
        )
    )

    meal.unpicked_unpaid_reservations = (
        meal
        .get_reservations_query()
        .filter(
            order__paid=False,
            order__confirmed=True,
            order__canceled=False,
        )
    )
    meal.unpicked_paid_reservations_count = (
        meal.unpicked_paid_reservations.count()
    )
    meal.unpicked_unpaid_reservations_count = (
        meal.unpicked_unpaid_reservations.count()
    )


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
