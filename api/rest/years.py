from rest_framework import serializers, viewsets

from .workshops import WorkshopSerializer
from ..models import PriceLevel, Year


class PriceLevelSerializer(serializers.ModelSerializer):
    takesEffectOn = serializers.DateField(source='takes_effect_on')

    class Meta:
        model = PriceLevel
        fields = (
            'id',
            'name',
            'year',
            'entryFee',
            'takesEffectOn',
        )


class YearSerializer(serializers.HyperlinkedModelSerializer):
    endDate = serializers.DateField(source='end_date')
    endFoodPickingAt = serializers.DateTimeField(source='end_food_picking_at')
    priceLevels = PriceLevelSerializer(source='price_levels', many=True)
    startDate = serializers.DateField(source='start_date')
    startSignupsAt = serializers.DateTimeField(source='start_date_of_signups')

    class Meta:
        model = Year
        fields = (
            'id',
            'year',
            'topic',
            'startDate',
            'endDate',
            'startSignupsAt',
            'endFoodPickingAt',
            'current',
            'priceLevels',
        )


class YearDetailSerializer(serializers.HyperlinkedModelSerializer):
    endDate = serializers.DateField(source='end_date')
    endFoodPickingAt = serializers.DateTimeField(source='end_food_picking_at')
    startDate = serializers.DateField(source='start_date')
    startSignupsAt = serializers.DateTimeField(source='start_date_of_signups')
    workshops = serializers.SerializerMethodField()

    class Meta:
        model = Year
        fields = (
            'id',
            'year',
            'topic',
            'startDate',
            'endDate',
            'startSignupsAt',
            'endFoodPickingAt',
            'current',
            'workshops',
        )

    def get_workshops(self, obj):
        queryset = obj.get_workshops().prefetch_related('lectors', 'photos')
        serializer = WorkshopSerializer(
            instance=queryset,
            many=True,
            context=self.context,
        )
        return serializer.data


class YearViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Year.objects.all()
    serializer_class = YearSerializer
    lookup_field = 'year'

    def get_serializer_class(self):
        return YearDetailSerializer if self.action == 'retrieve' else YearSerializer
