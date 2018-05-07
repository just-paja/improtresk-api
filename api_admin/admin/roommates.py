from api_roommates import models

from django.contrib.admin import SimpleListFilter
from django.db.models import Count, F

from ..models import BaseAdminModel, BaseInlineAdminModel


class RoomCapacityFilter(SimpleListFilter):
    title = 'Is available'
    parameter_name = 'available'

    def lookups(self, request, model_admin):
        return [
            (1, 'Yes'),
            (2, 'No'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.annotate(ppl_count=Count('inhabitants')).filter(
                ppl_count__lt=F('size'),
            )
        if self.value() == '2':
            return queryset.annotate(ppl_count=Count('inhabitants')).filter(
                ppl_count__gte=F('size'),
            )


class InhabitantAdmin(BaseInlineAdminModel):
    model = models.Inhabitant


class RoomAdmin(BaseAdminModel):
    list_display = ('number', 'accomodation_link', 'remaining_capacity', 'size')
    list_filter = (RoomCapacityFilter, 'accomodation__year', 'accomodation',)
    inlines = [
        InhabitantAdmin,
    ]


class RoomMateAdmin(BaseAdminModel):
    list_display = ('id', 'participant_link', 'room_link')
    list_filter = ('room__accomodation__year', 'room__accomodation',)
