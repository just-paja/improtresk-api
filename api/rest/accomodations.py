from django.shortcuts import get_object_or_404

from rest_framework import permissions, serializers, viewsets

from ..models import Accomodation, AccomodationDescription, AccomodationPhoto, Year


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
    hasRooms = serializers.SerializerMethodField(method_name='has_rooms')
    requiresIdentification = serializers.BooleanField(source='requires_identification')

    def has_rooms(self, obj):
        return obj.rooms.count() > 0

    class Meta:
        model = Accomodation
        fields = (
            'address',
            'id',
            'name',
            'desc',
            'capacity',
            'description',
            'price',
            'photos',
            'available',
            'requiresIdentification',
            'hasRooms',
        )


class AccomodationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AccomodationSerializer
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET',)

    def get_queryset(self):
        year = get_object_or_404(Year, year=self.kwargs.get('year', None))
        return Accomodation.objects.filter(year=year)
