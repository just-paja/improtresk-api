from django.shortcuts import get_object_or_404

from rest_framework import serializers, viewsets

from ..models import ScheduleEvent, Year


class ScheduleEventSerializer(serializers.ModelSerializer):
    endAt = serializers.DateTimeField(source='end_at')
    startAt = serializers.DateTimeField(source='start_at')

    class Meta:
        model = ScheduleEvent
        fields = (
            'id',
            'name',
            'year',
            'startAt',
            'endAt',
            'workshops',
            'performer',
        )


class ScheduleEventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ScheduleEventSerializer

    def get_queryset(self):
        year = get_object_or_404(Year, year=self.kwargs.get('year', None))
        return year.events
