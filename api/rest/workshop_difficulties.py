from rest_framework import serializers, viewsets

from ..models import WorkshopDifficulty


class WorkshopDifficultySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkshopDifficulty
        fields = (
            'id',
            'name',
            'slug',
            'description',
        )


class WorkshopDifficultyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkshopDifficulty.objects.all()
    serializer_class = WorkshopDifficultySerializer
