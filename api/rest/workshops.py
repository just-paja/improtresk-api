from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets

from .workshop_lectors import WorkshopLectorSerializer
from ..models import Workshop, WorkshopPhoto, WorkshopPrice, Year


class WorkshopPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopPrice
        fields = (
            'id',
            'price_level',
            'price',
            'workshop',
        )


class WorkshopPhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkshopPhoto
        fields = (
            'id',
            'image',
            'desc',
            'height',
            'width',
        )


class WorkshopSerializer(serializers.ModelSerializer):
    prices = WorkshopPriceSerializer(many=True)
    lectors = WorkshopLectorSerializer(
        source='workshoplector_set',
        many=True,
        read_only=True,
    )
    photos = WorkshopPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Workshop
        fields = (
            'id',
            'capacity',
            'name',
            'desc',
            'difficulty',
            'photos',
            'lectors',
            'prices',
        )


class WorkshopViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WorkshopSerializer

    def get_queryset(self):
        year = get_object_or_404(Year, year=self.kwargs.get('year', None))
        return year.get_workshops().prefetch_related('lectors', 'photos')
