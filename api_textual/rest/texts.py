from rest_framework import serializers, viewsets

from .. import models


class TextSerializer(serializers.HyperlinkedModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at')

    class Meta:
        model = models.Text
        fields = (
            'id',
            'name',
            'slug',
            'text',
            'createdAt',
        )


class TextViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Text.objects.all()
    serializer_class = TextSerializer
