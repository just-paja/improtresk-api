from rest_framework import serializers, viewsets

from .workshop_difficulties import WorkshopDifficultySerializer
from .workshop_lectors import WorkshopLectorSerializer
from ..models import Workshop


class WorkshopSerializer(serializers.HyperlinkedModelSerializer):
    difficulty = WorkshopDifficultySerializer()
    lectors = WorkshopLectorSerializer(
        source='workshoplector_set',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Workshop
        fields = (
            'id',
            'name',
            'desc',
            'difficulty',
            'photos',
            'lectors',
        )


class WorkshopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
