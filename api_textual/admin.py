from api.admin import BaseAdminModel, BaseInlineAdminModel

from django.contrib import admin

from . import models


class TextPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for Food photos."""

    model = models.TextPhoto


@admin.register(models.Text)
class TextAdmin(BaseAdminModel):
    """Admin model for Text."""

    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        TextPhotoInlineAdmin,
    ]
