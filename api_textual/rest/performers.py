from api.fields import VISIBILITY_PUBLIC

from api.models import Year

from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets

from .. import models


class PerformerLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PerformerLink
        fields = (
            'id',
            'name',
            'service',
            'address',
            'performer',
        )


class PerformerPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PerformerPhoto
        fields = (
            'id',
            'image',
            'desc',
            'height',
            'width',
        )


class PerformerSerializer(serializers.ModelSerializer):
    links = PerformerLinkSerializer(many=True, read_only=True)
    photos = PerformerPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = models.Performer
        fields = (
            'id',
            'name',
            'links',
            'photos',
            'slug',
            'text',
            'year',
        )


class PerformerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PerformerSerializer

    def get_queryset(self):
        year = get_object_or_404(Year, year=self.kwargs.get('year', None))
        return year.performers.filter(visibility=VISIBILITY_PUBLIC)
