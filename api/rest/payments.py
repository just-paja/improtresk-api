
from rest_framework import serializers

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
