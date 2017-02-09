from rest_framework import permissions, serializers, viewsets

from .workshops import WorkshopSerializer
from ..models import Workshop, Year


class YearSerializer(serializers.HyperlinkedModelSerializer):
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')
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
            'current',
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
        ids = [price.id for price in obj.price_levels.prefetch_related('workshop_prices')]
        queryset = Workshop.objects\
            .distinct()\
            .filter(prices__id__in=ids)\
            .prefetch_related('lectors', 'photos')
        serializer = WorkshopSerializer(instance=queryset, many=True)
        return serializer.data


class YearViewSet(viewsets.ModelViewSet):
    queryset = Year.objects.all()
    serializer_class = YearSerializer
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET',)

    def get_serializer_class(self):
        return YearDetailSerializer if self.action == 'retrieve' else YearSerializer
