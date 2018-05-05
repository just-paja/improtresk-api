from api_roommates import models

from ..models import BaseAdminModel, BaseInlineAdminModel


class InhabitantAdmin(BaseInlineAdminModel):
    model = models.Inhabitant


class RoomAdmin(BaseAdminModel):
    list_display = ('number', 'accomodation_link', 'size')
    list_filter = ('accomodation__year', 'accomodation',)
    inlines = [
        InhabitantAdmin,
    ]


class RoomMateAdmin(BaseAdminModel):
    list_display = ('id', 'participant_link', 'room_link')
    list_filter = ('room__accomodation__year', 'room__accomodation',)
