from rest_framework import serializers, viewsets

from .. import models


class NewsPhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.NewsPhoto
        fields = (
            'image',
            'desc',
            'height',
            'width',
        )


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at')
    photos = NewsPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = models.News
        fields = (
            'id',
            'name',
            'photos',
            'slug',
            'text',
            'createdAt',
        )


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.News.objects.all()
    serializer_class = NewsSerializer
