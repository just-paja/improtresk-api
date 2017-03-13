from rest_framework import permissions, serializers, viewsets

from ..models import Accomodation, AccomodationPhoto


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


class AccomodationSerializer(serializers.HyperlinkedModelSerializer):
    photos = AccomodationPhotoSerializer(many=True, read_only=True)
    available = serializers.IntegerField(source='available_capacity')

    class Meta:
        model = Accomodation
        fields = (
            'id',
            'name',
            'desc',
            'capacity',
            'price',
            'photos',
            'available',
        )


class AccomodationCapacitySerializer(serializers.ModelSerializer):
    available_capacity = serializers.Field

    class Meta:
        model = Accomodation
        fields = (
            'id',
            'capacity',
            'available_capacity',
            'number_of_unpaid_reservations',
            'number_of_reservations',
        )


class AccomodationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Accomodation.objects.all()
    serializer_class = AccomodationSerializer
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET',)


class AccomodationCapacityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Accomodation.objects.all()
    serializer_class = AccomodationCapacitySerializer
