from rest_framework import serializers, viewsets

from .polls import PollSerializer

from .. import models


class NewsPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NewsPhoto
        fields = (
            'image',
            'desc',
            'height',
            'width',
        )


class NewsSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at')
    updatedAt = serializers.DateTimeField(source='updated_at')
    photos = NewsPhotoSerializer(many=True, read_only=True)
    poll = PollSerializer(many=False)

    class Meta:
        model = models.News
        fields = (
            'id',
            'name',
            'photos',
            'poll',
            'slug',
            'text',
            'createdAt',
            'updatedAt',
        )


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.News.objects.all()
    serializer_class = NewsSerializer
