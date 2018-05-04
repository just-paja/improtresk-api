from django.http import Http404
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Order, Participant
from ..models import Inhabitant, Room


class InhabitantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='participant.name', read_only=True)
    participant_id = serializers.IntegerField(source='participant.pk', read_only=True)

    class Meta:
        model = Inhabitant
        fields = ('id', 'name', 'participant_id')


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


class RoomViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = RoomSerializer

    def get_queryset(self):
        try:
            self.participant = self.request.user.participant
        except Participant.DoesNotExist:
            raise Http404()
        paid_orders = self.participant.orders.filter(paid=True, canceled=False)
        self.reservations = [order.reservation.pk for order in paid_orders]
        return Room.objects.prefetch_related('accomodation__reservation_set').filter(
            accomodation__reservation__in=self.reservations
        )

    def get_room(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Room.DoesNotExist:
            raise Http404()

    @action(methods=['get'], detail=True)
    def inhabitants(self, request, pk=None):
        room = self.get_room(pk)
        serializer = InhabitantSerializer(room.inhabitants, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def join(self, request, pk=None):
        room = self.get_room(pk)
        if room.inhabitants.count() < room.size:
            inhabitant = Inhabitant(
                room=room,
                participant=self.participant
            )
            other_rooms = self.participant.inhabited_rooms.filter(
                room__accomodation__year=room.accomodation.year
            ).all()
            for deprecated_room in other_rooms:
                deprecated_room.delete()
            inhabitant.save()
            serializer = RoomSerializer(self.get_queryset(), many=True)
            return Response(serializer.data)
        return Response(
            {'errors': ['room-is-full']},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['put'], detail=True)
    def leave(self, request, pk=None):
        room = self.get_room(pk)
        inhabitant = room.inhabitants.filter(participant=self.participant).first()
        if inhabitant:
            inhabitant.delete()
            serializer = RoomSerializer(self.get_queryset(), many=True)
            return Response(serializer.data)
        return Response(
            {'errors': ['not-in-the-room']},
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderRoomViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = RoomSerializer

    def get_queryset(self):
        try:
            self.participant = self.request.user.participant
            self.order = Order.objects.get(pk=self.kwargs.get('order'))
        except (Participant.DoesNotExist, Order.DoesNotExist):
            raise Http404()
        if self.order.participant.pk != self.participant.pk:
            raise Http404()
        if not self.order.reservation or not self.order.reservation.accomodation:
            return Room.objects.none()
        return self.order.reservation.accomodation.rooms
