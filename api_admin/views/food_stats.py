from api.models import (
    Food,
    Soup,
    Year,
)

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone


def get_unpicked_reservations(meal, paid):
    query = meal.get_reservations_query().distinct().filter(
        order__paid=paid,
        order__year=meal.year,
        order__confirmed=True,
        order__canceled=False,
    ).filter(
        Q(mealreservation__food__isnull=True) |
        Q(mealreservation__soup__isnull=True),
    )
    if not paid:
        query = query.filter(ends_at__lte=timezone.now())
    return query


def get_picked_reservations(meal, food, paid):
    query = food.get_reservations_query().filter(
        order__year=meal.year,
        order__paid=paid,
        order__confirmed=True,
        order__canceled=False,
    )
    if not paid:
        query = query.filter(ends_at__lte=timezone.now())
    return query


def update_food_stats(meal, mixed_food):
    for food in mixed_food:
        food.paid_reservations = get_picked_reservations(meal, food, True).count()
        food.unpaid_reservations = get_picked_reservations(meal, food, False).count()


def update_meal_stats(meal):
    unpicked_paid = get_unpicked_reservations(meal, True)
    unpicked_unpaid = get_unpicked_reservations(meal, False)
    meal.unpicked_paid_reservations_count = unpicked_paid.count()
    meal.unpicked_paid_reservations = unpicked_paid.all()
    meal.unpicked_unpaid_reservations_count = unpicked_unpaid.count()
    meal.unpicked_unpaid_reservations = unpicked_unpaid.all()


@staff_member_required
def food_stats(request, festivalId):
    festival = Year.objects.get(pk=festivalId)
    meals = festival.meals.all()
    order = []

    for meal in meals:
        soups = Soup.objects.filter(meal=meal.id).all()
        foods = Food.objects.filter(meal=meal.id).all()
        order += soups
        order += foods
        update_meal_stats(meal)
        update_food_stats(meal, soups)
        update_food_stats(meal, foods)

    return render(
        request,
        'stats/food_stats.html',
        {
            'festival': festival,
            'meals': meals,
            'order': order,
        },
    )
