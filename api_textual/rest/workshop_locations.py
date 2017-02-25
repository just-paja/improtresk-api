from api.models import Year

from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets

from .. import models


class WorkshopLocationPhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.WorkshopLocationPhoto
        fields = (
            'image',
            'desc',
            'height',
            'width',
        )


class WorkshopLocationSerializer(serializers.HyperlinkedModelSerializer):
    photos = WorkshopLocationPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = models.WorkshopLocation
        fields = (
            'id',
            'name',
            'address',
            'photos',
            'slug',
            'text',
        )


class WorkshopLocationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WorkshopLocationSerializer

    def get_queryset(self):
        year = get_object_or_404(Year, year=self.kwargs.get('year', None))
        return year.get_locations().prefetch_related('photos')
