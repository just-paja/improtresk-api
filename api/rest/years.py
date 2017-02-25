from rest_framework import serializers, viewsets

from .workshops import WorkshopSerializer
from ..models import PriceLevel, Year


class PriceLevelSerializer(serializers.ModelSerializer):
    takesEffectOn = serializers.DateTimeField(source='takes_effect_on')

    class Meta:
        model = PriceLevel
        fields = (
            'id',
            'name',
            'year',
            'takesEffectOn',
        )


class YearSerializer(serializers.HyperlinkedModelSerializer):
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')
    startSignupsAt = serializers.DateTimeField(source='start_date_of_signups')
    priceLevels = PriceLevelSerializer(source='price_levels', many=True)

    class Meta:
        model = Year
        fields = (
            'id',
            'year',
            'topic',
            'startDate',
            'endDate',
            'startSignupsAt',
            'current',
            'priceLevels',
        )


class YearDetailSerializer(serializers.HyperlinkedModelSerializer):
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')
    workshops = serializers.SerializerMethodField()

    class Meta:
        model = Year
        fields = (
            'id',
            'year',
            'topic',
            'startDate',
            'endDate',
            'current',
            'workshops',
        )

    def get_workshops(self, obj):
        queryset = obj.get_workshops().prefetch_related('lectors', 'photos')
        serializer = WorkshopSerializer(instance=queryset, many=True)
        return serializer.data


class YearViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Year.objects.all()
    serializer_class = YearSerializer
    lookup_field = 'year'

    def get_serializer_class(self):
        return YearDetailSerializer if self.action == 'retrieve' else YearSerializer
