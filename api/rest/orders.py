from django.db.models import Sum

from rest_framework import permissions, response, serializers, status, viewsets

from .reservations import ReservationSerializer

from ..models import Meal, MealReservation, Order, Reservation, Workshop, Year


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    reservation = ReservationSerializer(
        many=False,
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
        )


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.none()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        if user.participant:
            return Order.objects\
                .filter(participant=user.participant)\
                .prefetch_related('reservation')


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


class CreateOrderViewSet(viewsets.ViewSet):
    serializer_class = CreateOrderSerializer

    def create(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.user = request.user
        if serializer.user.participant and serializer.is_valid():
            serializer.save()
            return response.Response(
                OrderSerializer(instance=serializer.instance, context={'request': request}).data,
            )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
