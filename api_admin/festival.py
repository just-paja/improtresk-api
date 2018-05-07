from api import models as models_api
from api_roommates import models as models_roommates
from api_textual import models as models_textual
from checkin import models as models_checkin

from oauth2_provider import admin as oauth_admin
from django.contrib.auth import admin as auth_admin
from django.conf.urls import url
from django.contrib.admin import AdminSite

from . import views
from .admin import (
    accomodation,
    checkin,
    festival,
    food,
    lectors,
    news,
    orders,
    participants,
    performers,
    polls,
    roommates,
    schedule,
    texts,
    workshops,
)


class FestivalAdminSite(AdminSite):
    def get_urls(self):
        return (
            super(FestivalAdminSite, self).get_urls() +
            [
                url(r'^stats/$', views.index, name='stats'),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/accomodation-registrations$',
                    views.accomodation_inhabitant_list,
                    name='stats-accomodation-registrations',
                ),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/food$',
                    views.food_stats,
                    name='stats-food',
                ),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/numbers$',
                    views.numbers,
                    name='stats-numbers',
                ),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/food-per-location$',
                    views.food_delivery,
                    name='stats-food-per-location',
                ),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/workshops$',
                    views.workshop_capacity,
                    name='stats-workshops',
                ),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/workshops-participants$',
                    views.workshop_participants,
                    name='stats-workshops-participants',
                ),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/accounting$',
                    views.allowance_list,
                    name='stats-accounting',
                ),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/participant-teams$',
                    views.participant_teams,
                    name='stats-participant-teams',
                ),
                url(
                    r'^stats/(?P<festivalId>[0-9]+)/participants$',
                    views.participant_list,
                    name='stats-participants',
                ),
            ]
        )


festival_site = FestivalAdminSite()

festival_site.register(models_api.Accomodation, accomodation.AccomodationAdmin)
festival_site.register(models_api.Food, food.FoodAdmin)
festival_site.register(models_api.Lector, lectors.LectorAdmin)
festival_site.register(models_api.LectorRole, lectors.LectorRoleAdmin)
festival_site.register(models_api.Meal, food.MealAdmin)
festival_site.register(models_api.Order, orders.OrderAdmin)
festival_site.register(models_api.Participant, participants.ParticipantAdmin)
festival_site.register(models_api.Payment, orders.PaymentAdmin)
festival_site.register(models_api.PriceLevel, festival.PriceLevelAdmin)
festival_site.register(models_api.Reservation, orders.ReservationAdmin)
festival_site.register(models_api.Rules, festival.RulesAdmin)
festival_site.register(models_api.ScheduleEvent, schedule.ScheduleEventAdmin)
festival_site.register(models_api.Soup, food.SoupAdmin)
festival_site.register(models_api.Team, participants.TeamAdmin)
festival_site.register(models_api.Workshop, workshops.WorkshopAdmin)
festival_site.register(models_api.WorkshopDifficulty, workshops.WorkshopDifficultyAdmin)
festival_site.register(models_api.WorkshopPrice, workshops.WorkshopPriceAdmin)
festival_site.register(models_api.Year, festival.YearAdmin)
festival_site.register(models_checkin.Checkin, checkin.CheckinAdmin)
festival_site.register(models_textual.News, news.NewsAdmin)
festival_site.register(models_textual.Performer, performers.PerformerAdmin)
festival_site.register(models_textual.Poll, polls.PollAdmin)
festival_site.register(models_textual.Text, texts.TextAdmin)
festival_site.register(models_textual.TravelingTip, texts.TravelingTipAdmin)
festival_site.register(models_textual.WorkshopLocation, workshops.WorkshopLocationAdmin)

festival_site.register(oauth_admin.Application, oauth_admin.ApplicationAdmin)
festival_site.register(oauth_admin.Grant, oauth_admin.GrantAdmin)
festival_site.register(oauth_admin.AccessToken, oauth_admin.AccessTokenAdmin)
festival_site.register(oauth_admin.RefreshToken, oauth_admin.RefreshTokenAdmin)

festival_site.register(auth_admin.Group, auth_admin.GroupAdmin)
festival_site.register(auth_admin.User, auth_admin.UserAdmin)

festival_site.register(models_roommates.Room, roommates.RoomAdmin)
festival_site.register(models_roommates.Inhabitant, roommates.RoomMateAdmin)
