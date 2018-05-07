from ..models import BaseAdminModel


class CheckinAdmin(BaseAdminModel):
    """Admin model for Accomodation and its photos."""

    fields = []
    list_display = ('participant_link', 'created_at')
    search_fields = ('order__symvar', 'order__participant__name',)
