from api.admin import BaseAdminModel, BaseInlineAdminModel

from django.contrib import admin

from . import models


class AbstractTextAdmin(BaseAdminModel):
    """Admin model for Abstract Text."""

    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'updated_at')


class TextPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for Food photos."""

    model = models.TextPhoto


@admin.register(models.Text)
class TextAdmin(AbstractTextAdmin):
    """Admin model for Text."""

    inlines = [
        TextPhotoInlineAdmin,
    ]


class WorkshopLocationPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for WorkshopLocation photos."""

    model = models.WorkshopLocationPhoto


@admin.register(models.WorkshopLocation)
class WorkshopLocationAdmin(AbstractTextAdmin):
    """Admin model for Workshop location."""

    inlines = [
        WorkshopLocationPhotoInlineAdmin,
    ]
    list_display = ('name', 'address', 'updated_at')


class TravelingTipPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for TravelingTip photos."""

    model = models.TravelingTipPhoto


@admin.register(models.TravelingTip)
class TravelingTipAdmin(AbstractTextAdmin):
    """Admin model for Workshop location."""

    inlines = [
        TravelingTipPhotoInlineAdmin,
    ]


class NewsPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for TravelingTip photos."""

    model = models.NewsPhoto


@admin.register(models.News)
class NewsAdmin(AbstractTextAdmin):
    """Define admin model for News."""

    inlines = [
        NewsPhotoInlineAdmin,
    ]
