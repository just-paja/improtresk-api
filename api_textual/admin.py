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


class WorkshopLocationPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for WorkshopLocation photos."""

    model = models.WorkshopLocationPhoto


@admin.register(models.WorkshopLocation)
class WorkshopLocationAdmin(BaseAdminModel):
    """Admin model for Workshop location."""

    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        WorkshopLocationPhotoInlineAdmin,
    ]
