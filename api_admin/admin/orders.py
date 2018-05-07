from django.db.models import Q
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils import timezone

from api import models as models_api

from ..models import BaseAdminModel, BaseInlineAdminModel, DEFAULT_READONLY


class OrderReservationValidFilter(SimpleListFilter):
    title = 'Time valid'
    parameter_name = 'time_valid'

    def lookups(self, request, model_admin):
        return [
            (1, 'Yes'),
            (2, 'No'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(
                reservation__ends_at__gt=timezone.now(),
            )
        if self.value() == '2':
            return queryset.filter(
                Q(reservation__ends_at__lte=timezone.now()) |
                Q(reservation__ends_at__isnull=True)
            )


class MealReservationInlineAdmin(BaseInlineAdminModel):
    """Admin model for MealReservation."""

    model = models_api.MealReservation


class ReservationAdmin(BaseAdminModel):
    """Admin model for Reservations."""
    readonly_fields = ('participant_link', 'checkin_link')
    list_display = (
        'id',
        'participant_link',
        'order_link',
        'workshop',
        'accomodation',
        'price',
        'ends_at',
        'is_valid',
    )
    list_filter = (
        'order__year',
        'order__confirmed',
        'order__canceled',
        'order__paid',
        'meals',
    )
    inlines = [MealReservationInlineAdmin]
    autocomplete_fields = ('workshop_price', 'order',)
    search_fields = [
        'order__participant__name',
        'order__year__year',
        'accomodation__name',
        'workshop_price__workshop__name',
        'order__price'
    ]


class ReservationInlineAdmin(admin.StackedInline):
    """Inline admin model for Reservations."""
    model = models_api.Reservation


class OrderAdmin(BaseAdminModel):
    """Admin model for Orders."""

    list_display = (
        'symvar',
        'participant_link',
        'reservation_link',
        'price',
        'is_valid',
        'canceled',
        'paid',
        'created_at',
        'valid_until',
    )
    list_filter = (
        'year',
        'paid',
        'confirmed',
        'over_paid',
        'canceled',
        OrderReservationValidFilter,
    )
    list_select_related = True
    autocomplete_fields = ['participant']
    fields = [
        'year',
        'participant',
        'symvar',
        'checkin_link',
        'accomodation_info',
        'confirmed',
        'canceled',
        'paid',
        'over_paid',
        'price',
        'created_at',
        'updated_at',
    ]
    search_fields = [
        'participant__name',
        'participant__team__name',
        'price',
        'reservation__accomodation__name',
        'reservation__workshop_price__workshop__name',
        'symvar',
    ]
    inlines = [ReservationInlineAdmin]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                'participant',
                'symvar',
                'total_amount_received',
                'checkin_link',
            ] + DEFAULT_READONLY
        return [
            'symvar',
            'total_amount_received',
            'checkin_link',
        ] + DEFAULT_READONLY


class PaymentAdmin(BaseAdminModel):
    """Admin model for Food and its photos."""
    list_display = (
        'ident',
        'order',
        'user_identification',
        'symvar',
        'symcon',
        'symspc',
        'amount',
        'sender',
        'bank',
        'message',
        'currency',
        'received_at',
    )
    list_filter = ('bank',)

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
                'received_at',
            ]
        return super(PaymentAdmin, self).get_readonly_fields(
            request,
            obj,
        )
