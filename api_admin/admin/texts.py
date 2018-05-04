from api_textual import models as models_text

from ..models import BaseTextAdminModel, BaseInlineAdminModel


class TextPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for Food photos."""

    model = models_text.TextPhoto


class TextAdmin(BaseTextAdminModel):
    """Admin model for Text."""
    list_filter = ('lang', 'category')
    inlines = [
        TextPhotoInlineAdmin,
    ]


class TravelingTipPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for TravelingTip photos."""

    model = models_text.TravelingTipPhoto


class TravelingTipAdmin(BaseTextAdminModel):
    """Admin model for Workshop location."""
    fields = [
        'name',
        'slug',
        'lang',
        'text',
    ]
    inlines = [
        TravelingTipPhotoInlineAdmin,
    ]
