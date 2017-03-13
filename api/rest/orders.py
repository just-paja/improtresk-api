from django.db.models import Sum

from rest_framework import mixins, permissions, response, serializers, status, viewsets

from .payments import PaymentSerializer
from .reservations import ReservationSerializer

from ..models import Meal, MealReservation, Order, Reservation, Workshop, Year


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    reservation = ReservationSerializer(
        many=False,
        read_only=True,
    )
    payments = PaymentSerializer(
        source="payment_set",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = (
            'id',
            'participant',
            'symvar',
            'price',
            'paid',
            'canceled',
            'reservation',
            'payments',
        )


class CreateOrderSerializer(serializers.Serializer):
    workshop = serializers.IntegerField()
    meals = serializers.ListField()
    accomodation = serializers.IntegerField()
    year = serializers.IntegerField()

    def create(self, validated_data):
        workshop = Workshop.objects.get(id=validated_data['workshop'])
        year = Year.objects.get(year=validated_data['year'])
        workshop_price = workshop.get_actual_workshop_price(year)
        meals = Meal.objects.filter(id__in=validated_data['meals'])
        meals_price = meals.aggregate(Sum('price'))['price__sum']
        order = Order.objects.create(
            participant=self.user,
            price=workshop_price.price + meals_price,
        )
        reservation = Reservation.objects.create(
            accomodation_id=validated_data['accomodation'],
            workshop_price=workshop_price,
            order=order,
        )
        for meal in meals:
            MealReservation.objects.create(
                meal=meal,
                reservation=reservation,
            )
        return order


class OrderViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        if user.participant:
            return Order.objects\
                .filter(participant=user.participant)\
                .prefetch_related('reservation')

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        if order.participant != request.user:
            return response.Response(
                "Requested object doesn't belong to authentificated user",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if 'confirm' in request.GET:
            order.confirm()
            order.refresh_from_db()
        return super().retrieve(request, *args, **kwargs)

    def create(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.user = request.user
        if serializer.user.participant and serializer.is_valid():
            serializer.save()
            return response.Response(
                OrderSerializer(instance=serializer.instance, context={'request': request}).data,
            )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
