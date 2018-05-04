from api import models as models_api

from ..models import BaseAdminModel, BaseInlineAdminModel, FoodAdminMixin


class FoodPhotoAdmin(BaseInlineAdminModel):
    """Admin model for Food photos."""

    model = models_api.FoodPhoto


class FoodAdmin(FoodAdminMixin, BaseAdminModel):
    """Admin model for Food and its photos."""

    inlines = [
        FoodPhotoAdmin,
    ]


class SoupAdmin(FoodAdminMixin, BaseAdminModel):
    """Admin model for Food and its photos."""

    inlines = [
        FoodPhotoAdmin,
    ]


class MealAdmin(BaseAdminModel):
    """Admin model for Meal."""
    list_filter = ('year', 'visibility',)
    list_display = (
        'name',
        'price',
        'date',
        'visibility',
    )
