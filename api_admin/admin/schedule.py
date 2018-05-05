from ..models import BaseAdminModel


class ScheduleEventAdmin(BaseAdminModel):
    """Define admin model for Schedule Events."""

    list_display = ('name', 'location_name', 'start_at', 'end_at')
    list_filter = ('year',)
    autocomplete_fields = ('performer', 'workshops')
    search_fields = [
        'name',
        'location_name',
    ]
