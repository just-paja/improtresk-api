from api_textual import models as models_text

from ..models import BaseTextAdminModel, BaseInlineAdminModel


class NewsPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for TravelingTip photos."""

    model = models_text.NewsPhoto


class NewsAdmin(BaseTextAdminModel):
    """Define admin model for News."""
    fields = [
        'name',
        'slug',
        'lang',
        'text',
    ]
    inlines = [
        NewsPhotoInlineAdmin,
    ]
