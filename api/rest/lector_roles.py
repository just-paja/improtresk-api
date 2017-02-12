from rest_framework import serializers, viewsets

from ..models import LectorRole


class LectorRoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LectorRole
        fields = (
            'id',
            'name',
        )


class LectorRoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LectorRole.objects.all()
    serializer_class = LectorRoleSerializer
