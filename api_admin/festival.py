from api import models as models_api
from oauth2_provider import admin as oauth_admin

from api_textual import models as models_text
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.conf.urls import url
from django.contrib.admin import AdminSite

from .models import (
    BaseAdminModel,
    BaseInlineAdminModel,
    BaseTextAdminModel,
    DEFAULT_READONLY,
    FoodAdminMixin,
)

from .stats_views import (
    accounting,
    food,
    food_per_location,
    index,
    participant_list,
    workshops,
)


class FestivalAdminSite(AdminSite):
    def get_urls(self):
        return (
            super(FestivalAdminSite, self).get_urls() +
            [
                url(r'^stats/$', index),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/food$',
                    food,
                    name='stats-food',
                ),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/food-per-location$',
                    food_per_location,
                    name='stats-food-per-location',
                ),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/workshops$',
                    workshops,
                    name='stats-workshops',
                ),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/accounting$',
                    accounting,
                    name='stats-accounting',
                ),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/participants$',
                    participant_list,
                    name='stats-participants',
                ),
            ]
        )


class LectorPhotoAdmin(BaseInlineAdminModel):
    """Admin model for Lector photos."""

    model = models_api.LectorPhoto


class LectorAdmin(BaseAdminModel):
    """Admin model for Lectors and their photos."""

    inlines = [
        LectorPhotoAdmin,
    ]


class LectorRoleAdmin(BaseAdminModel):
    """Admin model for Lector roles."""

    prepopulated_fields = {'slug': ('name',)}


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


class AccomodationDescriptionAdmin(BaseInlineAdminModel):
    """Admin model for Accomodation photos."""

    model = models_api.AccomodationDescription


class AccomodationPhotoAdmin(BaseInlineAdminModel):
    """Admin model for Accomodation photos."""

    model = models_api.AccomodationPhoto


class AccomodationAdmin(BaseAdminModel):
    """Admin model for Accomodation and its photos."""

    inlines = [
        AccomodationDescriptionAdmin,
        AccomodationPhotoAdmin,
    ]
    fields = [
        'year',
        'name',
        'price',
        'visibility',
        'capacity',
    ]
    list_display = ('name', 'year', 'capacity', 'price', 'visibility')
    list_filter = ('year', 'visibility',)


class FoodPhotoAdmin(BaseInlineAdminModel):
    """Admin model for Food photos."""

    model = models_api.FoodPhoto


class FoodAdmin(FoodAdminMixin, BaseAdminModel):
    """Admin model for Food and its photos."""

    list_filter = ('meal',)
    inlines = [
        FoodPhotoAdmin,
    ]


class SoupAdmin(FoodAdminMixin, BaseAdminModel):
    """Admin model for Food and its photos."""

    list_filter = ('meal',)
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


class ParticipantWorkshopAdmin(BaseInlineAdminModel):
    """Admin model for Participant workshop assignment."""

    model = models_api.ParticipantWorkshop
    exclude = [
        'created_at',
    ]


class ParticipantStayAdmin(BaseInlineAdminModel):
    """Admin model for Participant workshop assignment."""

    model = models_api.ParticipantStay
    exclude = [
        'created_at',
    ]


class ParticipantAdmin(BaseAdminModel):
    """Admin model for Participants."""

    inlines = [
        ParticipantWorkshopAdmin,
        ParticipantStayAdmin,
    ]
    readonly_fields = [
        'password',
        'last_login',
    ]
    exclude = [
        'is_superuser',
        'groups',
        'user_permissions',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'assigned_workshop',
    ]
    list_display = (
        'name',
        'team',
        'email',
        'newsletter',
        'created_at',
    )
    list_filter = ('team', 'newsletter')
    search_fields = ['name', 'email']


class MealReservationInlineAdmin(BaseInlineAdminModel):
    """Admin model for MealReservation."""

    model = models_api.MealReservation


class ReservationAdmin(BaseAdminModel):
    """Admin model for Reservations."""
    readonly_fields = ('participant',)
    list_display = (
        'participant',
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
        'workshop_price',
        'accomodation',
        'meals',
    )
    inlines = [MealReservationInlineAdmin]


class ReservationInlineAdmin(admin.StackedInline):
    """Inline admin model for Reservations."""
    model = models_api.Reservation


class OrderAdmin(BaseAdminModel):
    """Admin model for Orders."""

    list_display = (
        'participant',
        'symvar',
        'created_at',
        'price',
        'canceled',
        'paid',
        'over_paid',
    )
    list_filter = ('year', 'paid', 'over_paid', 'canceled')
    fields = [
        'year',
        'participant',
        'symvar',
        'accomodation_info',
        'confirmed',
        'canceled',
        'paid',
        'over_paid',
        'price',
        'created_at',
        'updated_at',
    ]
    inlines = [ReservationInlineAdmin]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                'participant',
                'symvar',
                'total_amount_received',
            ] + DEFAULT_READONLY
        return [
            'symvar',
            'total_amount_received',
        ] + DEFAULT_READONLY


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


class TeamAdmin(BaseAdminModel):
    """Admin model for Teams."""

    list_display = (
        'id',
        'name',
        'visibility',
        'desc',
    )


class RulesAdmin(BaseAdminModel):
    """Define admin model for Rules."""

    list_display = ('year', 'created_at')
    list_filter = ('year',)


class ScheduleEventAdmin(BaseAdminModel):
    """Define admin model for Rules."""

    list_display = ('name', 'year', 'start_at', 'end_at')
    list_filter = ('year',)


class TextPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for Food photos."""

    model = models_text.TextPhoto


class TextAdmin(BaseTextAdminModel):
    """Admin model for Text."""
    list_filter = ('lang', 'category')
    inlines = [
        TextPhotoInlineAdmin,
    ]


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


class TravelingTipPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for TravelingTip photos."""

    model = models_text.TravelingTipPhoto


class TravelingTipAdmin(BaseTextAdminModel):
    """Admin model for Workshop location."""
    fields = [
        'name',
        'slug',
        'lang',
        'text',
    ]
    inlines = [
        TravelingTipPhotoInlineAdmin,
    ]


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


class LinkInlineAdmin(BaseInlineAdminModel):
    """Admin model for Links."""

    model = models_text.PerformerLink


class PerformerDescriptionInlineAdmin(BaseInlineAdminModel):
    """Admin model for TravelingTip photos."""

    model = models_text.PerformerDescription


class PerformerPhotoInlineAdmin(BaseInlineAdminModel):
    """Admin model for TravelingTip photos."""

    model = models_text.PerformerPhoto


class PerformerAdmin(BaseAdminModel):
    """Define admin model for Performer."""

    list_display = ('name', 'year', 'visibility')
    exclude = ('links',)
    inlines = [
        LinkInlineAdmin,
        PerformerDescriptionInlineAdmin,
        PerformerPhotoInlineAdmin,
    ]


class PollAnswerInlineAdmin(BaseInlineAdminModel):
    """Inline admin for Poll Answers."""

    model = models_text.PollAnswer
    readonly_fields = ['get_vote_count']


class PollAdmin(BaseAdminModel):
    """Admin for Polls."""

    inlines = [
        PollAnswerInlineAdmin,
    ]
    list_display = (
        'question',
        'closed',
        'get_answer_count',
        'get_vote_count',
        'get_winning_answer',
        'get_last_vote_date',
        'updated_at',
    )
    readonly_fields = [
        'get_answer_count',
        'get_vote_count',
        'get_winning_answer',
        'get_last_vote_date',
    ] + DEFAULT_READONLY


festival_site = FestivalAdminSite()

festival_site.register(models_api.Accomodation, AccomodationAdmin)
festival_site.register(models_api.Food, FoodAdmin)
festival_site.register(models_api.Lector, LectorAdmin)
festival_site.register(models_api.LectorRole, LectorRoleAdmin)
festival_site.register(models_api.Meal, MealAdmin)
festival_site.register(models_api.Order, OrderAdmin)
festival_site.register(models_api.Participant, ParticipantAdmin)
festival_site.register(models_api.Payment, PaymentAdmin)
festival_site.register(models_api.Reservation, ReservationAdmin)
festival_site.register(models_api.Rules, RulesAdmin)
festival_site.register(models_api.ScheduleEvent, ScheduleEventAdmin)
festival_site.register(models_api.Soup, SoupAdmin)
festival_site.register(models_api.Team, TeamAdmin)
festival_site.register(models_api.Workshop, WorkshopAdmin)
festival_site.register(models_api.WorkshopDifficulty, WorkshopDifficultyAdmin)
festival_site.register(models_api.Year, YearAdmin)
festival_site.register(models_text.News, NewsAdmin)
festival_site.register(models_text.Performer, PerformerAdmin)
festival_site.register(models_text.Poll, PollAdmin)
festival_site.register(models_text.Text, TextAdmin)
festival_site.register(models_text.TravelingTip, TravelingTipAdmin)
festival_site.register(models_text.WorkshopLocation, WorkshopLocationAdmin)

festival_site.register(oauth_admin.Application, oauth_admin.ApplicationAdmin)
festival_site.register(oauth_admin.Grant, oauth_admin.GrantAdmin)
festival_site.register(oauth_admin.AccessToken, oauth_admin.AccessTokenAdmin)
festival_site.register(oauth_admin.RefreshToken, oauth_admin.RefreshTokenAdmin)

festival_site.register(auth_admin.Group, auth_admin.GroupAdmin)
festival_site.register(auth_admin.User, auth_admin.UserAdmin)
