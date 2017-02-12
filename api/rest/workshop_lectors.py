from rest_framework import serializers, viewsets

from ..models import WorkshopLector


class WorkshopLectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopLector
        fields = (
            'id',
            'lector',
            'role',
        )


class WorkshopLectorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkshopLector.objects.all()
    serializer_class = WorkshopLectorSerializer
