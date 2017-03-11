from rest_framework import serializers

from .accomodations import AccomodationSerializer
from .workshops import WorkshopPriceSerializer

from ..models import Food, Meal, MealReservation, Reservation


class MealSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Meal
        fields = (
            'name',
            'course',
            'price',
            'date',
        )


class FoodSerializer(serializers.HyperlinkedModelSerializer):
    meal = MealSerializer(many=False, read_only=True)

    class Meta:
        model = Food
        fields = (
            'id',
            'name',
            'meal',
        )


class MealReservationSerializer(serializers.HyperlinkedModelSerializer):
    food = FoodSerializer(many=False, read_only=True)

    class Meta:
        model = MealReservation
        fields = (
            'id',
            'food',
        )


class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    mealreservation_set = MealReservationSerializer(many=True, read_only=True)
    workshop_price = WorkshopPriceSerializer(many=False, read_only=True)
    accomodation = AccomodationSerializer(many=False, read_only=True)

    class Meta:
        model = Reservation
        fields = (
            'id',
            # 'ends_at',
            'mealreservation_set',
            'workshop_price',
            'accomodation',
        )
