
from rest_framework import mixins, serializers, viewsets

from ..models import Payment


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id',
            'symvar',
            'symcon',
            'symspc',
            'amount',
            'sender',
            'bank',
            'currency',
            'received_at',
            'message',
            'status',
        )


class PaymentStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id',
            'symvar',
            'status',
        )


class PaymentViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Payment.objects.none()
    serializer_class = PaymentStatusSerializer
    lookup_field = 'symvar'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        if user.participant:
            return Payment.objects\
                .filter(order__participant=user.participant)
