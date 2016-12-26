"""Site administration module."""
from django.contrib import admin
from .models import Accomodation, AccomodationPhoto, Food, FoodPhoto, \
    Lector, LectorPhoto, Payment, Participant, Workshop, WorkshopPhoto, Year


DEFAULT_READONLY = ['createdAt', 'updatedAt']


class BaseAdminModel(admin.ModelAdmin):
    """Base for all admin models."""

    def get_readonly_fields(self, request, obj=None):
        """Define default readonly fields."""
        return DEFAULT_READONLY


class BaseInlineAdminModel(admin.TabularInline):
    """Base for all inline admin models."""

    def get_readonly_fields(self, request, obj=None):
        """Define default readonly fields."""
        return DEFAULT_READONLY


class LectorPhotoAdmin(BaseInlineAdminModel):
    """Admin model for Lector photos."""

    model = LectorPhoto


@admin.register(Lector)
class LectorAdmin(BaseAdminModel):
    """Admin model for Lectors and their photos."""

    inlines = [
        LectorPhotoAdmin,
    ]


class WorkshopPhotoAdmin(BaseInlineAdminModel):
    """Admin model for Workshop photos."""

    model = WorkshopPhoto


@admin.register(Workshop)
class WorkshopAdmin(BaseAdminModel):
    """Admin model for Workshops and their photos."""

    inlines = [
        WorkshopPhotoAdmin,
    ]


class AccomodationPhotoAdmin(BaseInlineAdminModel):
    """Admin model for Accomodation photos."""

    model = AccomodationPhoto


@admin.register(Accomodation)
class AccomodationAdmin(BaseAdminModel):
    """Admin model for Accomodation and its photos."""

    inlines = [
        AccomodationPhotoAdmin,
    ]


class FoodPhotoAdmin(BaseInlineAdminModel):
    """Admin model for Food photos."""

    model = FoodPhoto


@admin.register(Food)
class FoodAdmin(BaseAdminModel):
    """Admin model for Food and its photos."""

    inlines = [
        FoodPhotoAdmin,
    ]


@admin.register(Payment)
class PaymentAdmin(BaseAdminModel):
    """Admin model for Food and its photos."""

    def get_readonly_fields(self, request, obj=None):
        """Define all read only fields."""
        if obj:
            return DEFAULT_READONLY + [
                'ident',
                'symvar',
                'symcon',
                'symspc',
                'amount',
                'sender',
                'bank',
                'message',
                'currency',
                'received',
                'message',
            ]
        return super(PaymentAdmin, self).get_readonly_fields(
            request,
            obj
        )


@admin.register(Participant)
class ParticipantAdmin(BaseAdminModel):
    """Admin model for Participants."""

    pass


@admin.register(Year)
class YearAdmin(BaseAdminModel):
    """Admin model for Years."""

    pass
