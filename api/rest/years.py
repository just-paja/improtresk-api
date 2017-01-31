from rest_framework import permissions, serializers, viewsets

from ..models import Year


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


class YearViewSet(viewsets.ModelViewSet):
    queryset = Year.objects.all()
    serializer_class = YearSerializer
    permission_classes = [permissions.AllowAny]
    allowed_methods = ('GET',)
