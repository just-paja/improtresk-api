from django.shortcuts import get_object_or_404

from rest_framework import serializers, status, viewsets
from rest_framework.response import Response

from ..models import Accomodation, Workshop, Year


class CapacitySerializer(serializers.ModelSerializer):
    def __init__(self, year, *args, **kwargs):
        super(*args, **kwargs)


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


class WorkshopCapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = (
            'id',
            'capacity',
            'available_capacity',
            'number_of_unpaid_reservations',
            'number_of_reservations',
        )


class CapacityViewSet(viewsets.ReadOnlyModelViewSet):

    def list(self, request, year=None):
        year = get_object_or_404(Year, year=year)

        accomodation_qs = Accomodation.objects.all()
        accomodation_serial = AccomodationCapacitySerializer(
            accomodation_qs,
            many=True,
        )

        workshops_qs = year.get_workshops()
        workshops_serial = WorkshopCapacitySerializer(
            workshops_qs,
            many=True,
        )

        return Response(
            {
                'accomodation': accomodation_serial.data,
                'workshops': workshops_serial.data,
            },
            status=status.HTTP_200_OK,
        )
