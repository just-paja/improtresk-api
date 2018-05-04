from api import models as models_api
from api_textual import models as models_text

from ..models import BaseAdminModel, BaseInlineAdminModel


class WorkshopPhotoAdmin(BaseInlineAdminModel):
    """Admin model for Workshop photos."""

    model = models_api.WorkshopPhoto


class WorkshopDifficultyAdmin(BaseAdminModel):
    """Admin model for Workshop difficulties."""

    prepopulated_fields = {'slug': ('name',)}


class WorkshopLectorInlineAdmin(BaseInlineAdminModel):
    """Inline admin model for Workshop lectors."""

    model = models_api.WorkshopLector


class WorkshopPriceInlineAdmin(BaseInlineAdminModel):
    """Inline admin for Workshop prices."""

    model = models_api.WorkshopPrice


class WorkshopAdmin(BaseAdminModel):
    """Admin model for Workshops and their photos."""

    inlines = [
        WorkshopPhotoAdmin,
        WorkshopLectorInlineAdmin,
        WorkshopPriceInlineAdmin,
    ]

    list_display = ('name', 'desc', 'difficulty', 'visibility')
    list_filter = ('year', 'visibility', 'difficulty')
    search_fields = ['name']


class WorkshopLocationDescriptionInlineAdmin(BaseInlineAdminModel):
    """Admin model for WorkshopLocation photos."""

    model = models_text.WorkshopLocationDescription


class WorkshopLocationPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for WorkshopLocation photos."""

    model = models_text.WorkshopLocationPhoto


class WorkshopLocationAdmin(BaseAdminModel):
    """Admin model for Workshop location."""

    inlines = [
        WorkshopLocationDescriptionInlineAdmin,
        WorkshopLocationPhotoInlineAdmin,
    ]
    list_display = ('name', 'address', 'updated_at')
