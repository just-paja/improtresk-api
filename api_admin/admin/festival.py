from api import models as models_api

from ..models import BaseAdminModel, BaseInlineAdminModel


class RulesAdmin(BaseAdminModel):
    """Define admin model for Rules."""

    list_display = ('year', 'created_at')
    list_filter = ('year',)


class PriceLevelAdmin(BaseAdminModel):
    search_fields = ('name', 'year')
    list_display = ('name', 'year', 'takes_effect_on')
    list_filter = ('year',)


class PriceLevelInlineAdmin(BaseInlineAdminModel):
    """Inline admin for Workshop prices."""

    model = models_api.PriceLevel


class YearAdmin(BaseAdminModel):
    """Admin model for Years."""

    inlines = [
        PriceLevelInlineAdmin,
    ]
    list_display = ('year', 'topic', 'current', 'start_date', 'end_date')
    list_filter = ('current',)
