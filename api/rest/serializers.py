from rest_framework import permissions, routers, serializers, viewsets

from ..models import Year


class YearSerializer(serializers.HyperlinkedModelSerializer):
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')
    startSignupsAt = serializers.DateField(source='start_date_of_signups')

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


class YearSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Year.objects.all()
    serializer_class = YearSerializer
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET',)


router = routers.DefaultRouter()
router.register(r'years', YearSet, base_name="gpxfile")
