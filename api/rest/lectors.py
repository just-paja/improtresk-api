from rest_framework import serializers, viewsets

from ..models import Lector, LectorPhoto


class LectorPhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LectorPhoto
        fields = (
            'id',
            'image',
            'desc',
        )


class LectorSerializer(serializers.HyperlinkedModelSerializer):
    photos = LectorPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Lector
        fields = (
            'id',
            'name',
            'about',
            'photos',
        )


class LectorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lector.objects.all()
    serializer_class = LectorSerializer
