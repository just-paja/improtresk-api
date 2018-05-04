from django.http import Http404
from rest_framework import serializers, viewsets

from api.models import Order, Participant
from ..models import Inhabitant, Room


class InhabitantSerializer(serializers.ModelSerializer):
    model = Inhabitant
    fields = (
        'id',
        'name',
    )


class RoomSerializer(serializers.ModelSerializer):
    inhabitants = InhabitantSerializer(many=True)

    class Meta:
        model = Room
        fields = (
            'id',
            'accomodation',
            'inhabitants',
            'number',
            'size',
        )


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        try:
            self.participant = self.request.user.participant
        except Participant.DoesNotExist:
            raise Http404()
        try:
            self.order = self.participant.orders.filter(
                paid=True,
                canceled=False,
                year__year=self.kwargs.get('year'),
            ).first()
        except Order.DoesNotExist:
            raise Http404()
        if not self.order:
            raise Http404()
        return self.order.reservation.accomodation.rooms
