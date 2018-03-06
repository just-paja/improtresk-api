from rest_framework import serializers, viewsets

from .. import models


class TextSerializer(serializers.HyperlinkedModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at')

    class Meta:
        model = models.Text
        fields = (
            'category',
            'createdAt',
            'id',
            'lang',
            'name',
            'slug',
            'text',
        )


class TextViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Text.objects.all()
    serializer_class = TextSerializer

    def get_queryset(self):
        lang = self.request.query_params.get('lang', None)
        category = self.request.query_params.get('category', None)
        queryset = self.queryset
        if lang:
            queryset = queryset.filter(lang=lang)
        if category:
            queryset = queryset.filter(category=category)
        return queryset
