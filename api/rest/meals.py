from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets

from ..models import Meal, Year


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = (
            'id',
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
