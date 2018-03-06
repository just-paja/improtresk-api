from rest_framework import permissions, serializers, viewsets

from ..models import Accomodation, AccomodationDescription, AccomodationPhoto


class AccomodationPhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccomodationPhoto
        fields = (
            'id',
            'image',
            'desc',
            'height',
            'width',
        )


class AccomodationDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccomodationDescription
        fields = (
            'id',
            'lang',
            'text',
        )


class AccomodationSerializer(serializers.HyperlinkedModelSerializer):
    photos = AccomodationPhotoSerializer(many=True, read_only=True)
    available = serializers.IntegerField(source='available_capacity')
    description = AccomodationDescriptionSerializer(
        many=True,
        read_only=True,
        source='descriptions',
    )

    class Meta:
        model = Accomodation
        fields = (
            'id',
            'name',
            'desc',
            'capacity',
            'description',
            'price',
            'photos',
            'available',
        )


class AccomodationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Accomodation.objects.all()
    serializer_class = AccomodationSerializer
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET',)
