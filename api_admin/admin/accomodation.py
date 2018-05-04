from api import models as models_api
from api_roommates import models as models_roommates

from ..models import BaseAdminModel, BaseInlineAdminModel


class AccomodationDescriptionAdmin(BaseInlineAdminModel):
    """Admin model for Accomodation photos."""

    model = models_api.AccomodationDescription


class AccomodationPhotoAdmin(BaseInlineAdminModel):
    """Admin model for Accomodation photos."""

    model = models_api.AccomodationPhoto


class AccomodationRoomAdmin(BaseInlineAdminModel):
    model = models_roommates.Room


class AccomodationAdmin(BaseAdminModel):
    """Admin model for Accomodation and its photos."""

    inlines = [
        AccomodationDescriptionAdmin,
        AccomodationPhotoAdmin,
        AccomodationRoomAdmin,
    ]
    fields = [
        'year',
        'name',
        'address',
        'price',
        'visibility',
        'capacity',
        'requires_identification',
    ]
    list_display = ('name', 'year', 'capacity', 'price', 'visibility')
    list_filter = ('year', 'visibility',)
