from rest_framework import serializers, viewsets

from .. import models


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at')

    class Meta:
        model = models.News
        fields = (
            'id',
            'name',
            'slug',
            'text',
            'createdAt',
        )


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.News.objects.all()
    serializer_class = NewsSerializer
