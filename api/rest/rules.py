from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route

from ..models import Rules, Year


class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rules
        fields = (
            'id',
            'text',
            'year',
        )


class RulesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RulesSerializer

    def get_queryset(self):
        year = get_object_or_404(Year, year=self.kwargs.get('year', None))
        return year.rules

    @list_route()
    def latest(self, request, *args, **kwargs):
        return Response(RulesSerializer(self.get_queryset().latest('created_at')).data)
