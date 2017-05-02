from rest_framework import serializers, viewsets

from .. import models


class TravelingTipPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TravelingTipPhoto
        fields = (
            'image',
            'desc',
            'height',
            'width',
        )


class TravelingTipSerializer(serializers.HyperlinkedModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at')
    photos = TravelingTipPhotoSerializer(many=True)

    class Meta:
        model = models.TravelingTip
        lookup_field = 'slug'
        fields = (
            'id',
            'name',
            'slug',
            'text',
            'photos',
            'createdAt',
        )


class TravelingTipViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.TravelingTip.objects.all()
    serializer_class = TravelingTipSerializer
    lookup_field = 'slug'
