from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from rest_framework import permissions, response, serializers, status, viewsets
from rest_framework.serializers import ValidationError

from .payments import PaymentSerializer
from .reservations import ReservationSerializer

from ..models import Food, Meal, MealReservation, Order, Reservation, Soup,\
    ParticipantStay, Workshop, Year, Accomodation


class OrderSerializer(serializers.ModelSerializer):
    accomodationInfo = serializers.BooleanField(source='accomodation_info')
    cancelled = serializers.BooleanField(source='canceled')
    createdAt = serializers.DateTimeField(source='created_at')
    reservation = ReservationSerializer(
        many=False,
        read_only=True,
    )
    payments = PaymentSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = (
            'accomodationInfo',
            'cancelled',
            'confirmed',
            'createdAt',
            'id',
            'paid',
            'participant',
            'payments',
            'price',
            'reservation',
            'symvar',
            'year',
        )


class CreateOrderSerializer(serializers.Serializer):
    workshop = serializers.IntegerField(
        required=False,
        allow_null=True,
        default=None,
    )
    meals = serializers.ListField()
    stayLength = serializers.ListField(required=False)
    accomodation = serializers.IntegerField()
    accomodationInfo = serializers.BooleanField(required=False)
    year = None

    def __init__(self, *args, **kwargs):
        try:
            self.year = Year.objects.filter(current=True).order_by('-year').first()
        except Year.DoesNotExist:
            self.year = None
        serializers.Serializer.__init__(self, *args, **kwargs)

    def validate(self, data):
        if not self.year:
            raise ValidationError('orders.noYearActive')
        openOrders = Order.objects.filter(
            canceled=False,
            participant=self.user.participant,
            year=self.year,
        ).count()
        if openOrders > 0:
            raise ValidationError('orders.alreadyHaveOne')

        return data

    def validate_accomodation(self, value):
        if not value:
            return
        accomodation = None
        try:
            accomodation = Accomodation.objects.get(id=value)
        except Accomodation.DoesNotExist:
            raise ValidationError('orders.invalidSelection')
        if accomodation.year and accomodation.year.id != self.year.id:
            raise ValidationError('orders.invalidSelection')
        if not accomodation.has_free_capacity():
            raise ValidationError('orders.noCapacity')
        return accomodation

    def validate_workshop(self, value):
        if not value:
            return
        workshop = None
        try:
            workshop = Workshop.objects.get(id=value)
        except Workshop.DoesNotExist:
            raise ValidationError('orders.invalidSelection')
        if workshop.year and workshop.year.id != self.year.id:
            raise ValidationError('orders.invalidSelection')
        if not workshop.has_free_capacity():
            raise ValidationError('orders.noCapacity')
        return workshop

    def create(self, validated_data): # noqa
        total_price = 0

        if 'stayLength' in validated_data and validated_data['stayLength']:
            price_level = self.year.get_actual_price_level()
            currentStay = ParticipantStay.objects.filter(
                participant=self.user.participant,
                year=self.year
            )
            for stay in currentStay:
                stay.delete()
            for day in validated_data['stayLength']:
                stay = ParticipantStay(
                    participant=self.user.participant,
                    year=self.year,
                    date=day,
                )
                stay.save()

            if price_level and not validated_data['workshop']:
                total_price += len(validated_data['stayLength']) * price_level.entryFee

        if validated_data['workshop']:
            workshop = validated_data['workshop']
            workshop_price = workshop.get_actual_workshop_price(self.year)
            total_price += workshop_price.price
        else:
            workshop = None
            workshop_price = None

        meals = Meal.objects.filter(id__in=validated_data['meals'])
        meals_price = meals.aggregate(Sum('price'))['price__sum']
        if meals_price:
            total_price += meals_price

        order = Order.objects.create(
            participant=self.user.participant,
            price=total_price,
            accomodation_info=validated_data.get('accomodationInfo', False),
            year=self.year,
        )
        reservation = Reservation.objects.create(
            accomodation=validated_data['accomodation'],
            workshop_price=workshop_price,
            order=order,
        )
        for meal in meals:
            MealReservation.objects.create(
                meal=meal,
                reservation=reservation,
            )
        reservation.update_price()
        return order

    def update(self, instance, validated_data):
        return super().update()


class OrderViewSet(viewsets.ModelViewSet):
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
                .prefetch_related('reservation')\
                .prefetch_related('payments')

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        if order.participant != request.user.participant:
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
        serializer.user = request.user.participant
        if serializer.user.participant and serializer.is_valid():
            serializer.save()
            return response.Response(
                OrderSerializer(
                    instance=serializer.instance,
                    context={'request': request},
                ).data,
            )
        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, pk=None, *args, **kwargs):
        order = Order.objects.filter(pk=pk).first()
        next_workshop = Workshop.objects\
            .filter(pk=request.data.get('workshop', None))\
            .first()

        if not order or not next_workshop:
            return response.Response(
                {'errors': ['unknown-object']},
                status=status.HTTP_404_NOT_FOUND,
            )

        if order.participant != request.user.participant:
            return response.Response(
                {'errors': ['must-be-owner']},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            reservation = order.reservation
        except ObjectDoesNotExist:
            reservation = None

        # get current order reservation or 404
        if not reservation or not reservation.workshop_price:
            return response.Response(
                {'errors': ['make-reservation-first']},
                status=status.HTTP_403_FORBIDDEN,
            )

        current_price_level = reservation.workshop_price.price_level
        current_workshop = reservation.workshop_price.workshop
        next_price = next_workshop.prices.filter(
            price_level=current_price_level,
        ).first()

        if not next_price:
            return response.Response(
                {'errors': ['no-matching-price-level']},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not next_workshop.has_free_capacity():
            return response.Response(
                {'errors': ['workshop-is-full']},
                status=status.HTTP_403_FORBIDDEN,
            )

        reservation.workshop_price = next_price
        reservation.save()

        participant = self.request.user.participant
        if participant.assigned_workshop == current_workshop:
            participant.assigned_workshop = next_workshop
            participant.save()

        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        if order.participant == request.user.participant and not order.paid:
            order.canceled = True
            order.save()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(
            {
                "messages": ["cannot-cancel"],
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class FoodField(serializers.Field):
    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return data


class ChangeOrderFoodSerializer(serializers.Serializer):
    food = FoodField(required=True)

    class Meta:
        field = ('food', )

    def set_order(self, order):
        self.order = order

    def validate_food(self, value):
        for reservation in value:
            food = reservation.get('food', None)
            soup = reservation.get('soup', None)
            mealReservation = reservation.get('mealReservation')
            mealSelection = mealReservation.meal
            if food:
                try:
                    mealFood = Food.objects.get(pk=food)
                except Food.DoesNotExist:
                    raise ValidationError('orders.invalidFoodSelection:%s' % food)
                if mealFood.meal.pk != mealSelection.pk:
                    raise ValidationError('orders.invalidFoodSelection:%s' % food)
            if soup:
                try:
                    mealSoup = Soup.objects.get(pk=soup)
                except Soup.DoesNotExist:
                    raise ValidationError('orders.invalidSoupSelection%s' % soup)
                if mealSoup.meal.pk != mealSelection.pk:
                    raise ValidationError('orders.invalidSoupSelection%s' % soup)

    def create(self, validated_data):
        for reservation in validated_data.get('food'):
            mealReservation = reservation.get('mealReservation')
            food = reservation.get('food')
            soup = reservation.get('soup')
            mealReservation.food = Food.objects.get(pk=food) if food else None
            mealReservation.soup = Soup.objects.get(pk=soup) if soup else None
            mealReservation.save()
        return self.order

    def update(self, instance, validated_data):
        return self.create(validated_data)

    def to_internal_value(self, data):
        food = data.get('food', None)
        if not food:
            return {'food': None}
        order_reservation = self.order.reservation
        meal_reservations = order_reservation.mealreservation_set.all()
        result = []
        for meal_id_str, choices in food.items():
            meal_id = int(meal_id_str)
            try:
                reservation = {
                    'mealReservation': next(
                        item for item in meal_reservations if item.meal.pk == meal_id
                    ),
                    'food': choices.get('food', None),
                    'soup': choices.get('soup', None),
                }
            except StopIteration:
                reservation = None
            if reservation:
                result.append(reservation)
        return {
            'food': result
        }


class OrdersFoodViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.none()
    permission_classes = [permissions.IsAuthenticated]
    serializer = ChangeOrderFoodSerializer

    def get_queryset(self):
        return Order.objects\
            .filter(participant=self.request.user.participant)\
            .prefetch_related('reservation')

    def update(self, request, pk=None, *args, **kwargs):
        order = Order.objects.filter(pk=pk).first()
        if not order:
            return response.Response(
                {'errors': ['unknown-object']},
                status=status.HTTP_404_NOT_FOUND,
            )

        if order.participant != request.user.participant:
            return response.Response(
                {'errors': ['must-be-owner']},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ChangeOrderFoodSerializer(data=request.data)
        serializer.set_order(order)
        if serializer.is_valid():
            serializer.save()
        else:
            return response.Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return response.Response(status=status.HTTP_204_NO_CONTENT)
