from rest_framework import serializers, viewsets

from ..models import WorkshopLector


class WorkshopLectorSerializer(serializers.ModelSerializer):
    lector = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name',
    )
    role = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )

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
