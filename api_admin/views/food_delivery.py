from api.models import Food, Soup, Year
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


def load_food_counts(festivalId, foods, location, soup=False):
    for food in foods:
        food.deliver = food.get_reservations_query().filter(
            order__year=festivalId,
            order__paid=True,
            order__confirmed=True,
            order__canceled=False,
            workshop_price__workshop__location=location,
        ).count()
    return foods


@staff_member_required
def food_delivery(request, festivalId):
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
            location.delivery += load_food_counts(festivalId, soups, location)
            location.delivery += load_food_counts(festivalId, foods, location, True)

    return render(
        request,
        'stats/food_delivery.html',
        {
            'festival': festival,
            'delivery': delivery,
        },
    )
