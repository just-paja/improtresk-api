from api import models as models_api

from ..models import BaseAdminModel, BaseInlineAdminModel


class LectorPhotoAdmin(BaseInlineAdminModel):
    """Admin model for Lector photos."""

    model = models_api.LectorPhoto


class LectorAdmin(BaseAdminModel):
    """Admin model for Lectors and their photos."""

    inlines = [
        LectorPhotoAdmin,
    ]
    search_fields = ['name']


class LectorRoleAdmin(BaseAdminModel):
    """Admin model for Lector roles."""

    prepopulated_fields = {'slug': ('name',)}
