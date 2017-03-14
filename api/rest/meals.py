from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets

from ..models import Food, Meal, Soup, Year

food_fields = (
    'id',
    'capacity',
    'meal',
    'name',
)


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = food_fields


class SoupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Soup
        fields = food_fields


class MealSerializer(serializers.ModelSerializer):
    food = serializers.SerializerMethodField()
    soups = serializers.SerializerMethodField()

    def get_food(self, meal):
        qs = Food.objects.filter(meal=meal)
        serializer = FoodSerializer(instance=qs, many=True)
        return serializer.data

    def get_soups(self, meal):
        qs = Soup.objects.filter(meal=meal)
        serializer = SoupSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Meal
        fields = (
            'id',
            'soups',
            'food',
            'name',
            'price',
            'date',
            'visibility',
            'year',
        )


class MealViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MealSerializer

    def get_queryset(self):
        year = get_object_or_404(Year, year=self.kwargs.get('year', None))
        return year.meals.all()
