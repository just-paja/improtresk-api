from api_textual import models as models_text

from ..models import BaseAdminModel, BaseInlineAdminModel


class LinkInlineAdmin(BaseInlineAdminModel):
    """Admin model for Links."""

    model = models_text.PerformerLink


class PerformerDescriptionInlineAdmin(BaseInlineAdminModel):
    """Admin model for TravelingTip photos."""

    model = models_text.PerformerDescription


class PerformerPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for TravelingTip photos."""

    model = models_text.PerformerPhoto


class PerformerAdmin(BaseAdminModel):
    """Define admin model for Performer."""

    list_display = ('name', 'year', 'visibility')
    list_filter = ('year',)
    exclude = ('links',)
    search_fields = ('name',)
    inlines = [
        LinkInlineAdmin,
        PerformerDescriptionInlineAdmin,
        PerformerPhotoInlineAdmin,
    ]
