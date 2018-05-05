"""Signup model."""
from django.conf import settings
from django.contrib import auth
from django.core import mail
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Count, Q, QuerySet
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .participantToken import PASSWORD_RESET, ParticipantToken
from .team import Team
from .workshop import Workshop


class ParticipantQuerySet(QuerySet):
    def annotate_workshop_count(self):
        return self.annotate(workshop_count=Count('workshops'))

    def annotate_meal_count(self):
        return self.annotate(meal_count=Count('orders__reservation__meals'))

    def filter_by_festival(self, festival):
        return self.filter(
            Q(orders__paid=True) |
            Q(orders__reservation__ends_at__gt=timezone.now()),
            orders__year=festival,
            orders__canceled=False,
        )

    def filter_with_workshop(self):
        return self.annotate_workshop_count().filter(workshop_count__gt=0)

    def filter_without_workshop(self):
        return self.annotate_workshop_count().filter(workshop_count=0)

    def filter_with_meal(self):
        return self.annotate_meal_count().filter(meal_count__gt=0)

    def filter_without_meal(self):
        return self.annotate_meal_count().filter(meal_count=0)


class Participant(Base, auth.models.User):
    """Stores participants."""
    USERNAME_FIELD = 'email'
    objects = ParticipantQuerySet.as_manager()

    name = models.CharField(max_length=255)
    address = models.CharField(
        verbose_name=_("Address"),
        max_length=255,
        blank=True,
        null=True,
    )
    id_number = models.CharField(
        verbose_name=_("ID Number"),
        max_length=255,
        blank=True,
        null=True,
    )
    team = models.ForeignKey(
        Team,
        verbose_name=_("Team"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    phone = models.CharField(max_length=255)
    birthday = models.DateField(
        verbose_name=_("Date of birthday"),
    )

    rules_accepted = models.BooleanField(
        default=False,
        verbose_name=_("Are rules accepted?"),
        help_text=_(
            "Does the participant accepted the rules of the festival?"
        ),
    )
    newsletter = models.BooleanField(default=False)
    assigned_workshop = models.ForeignKey(
        Workshop,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    is_staff = False

    def __str__(self):
        """Return name and status as string representation."""
        return "%s" % (self.name)

    @property
    def team_name(self):
        return self.team.name

    @team_name.setter
    def team_name(self, name):
        self.team, _ = Team.objects.get_or_create(name=name)

    def request_password_reset(self):
        self.tokens.filter(token_type=PASSWORD_RESET).update(used=True)
        token = ParticipantToken.objects.create(
            participant=self,
            token_type=PASSWORD_RESET,
        )
        mail.send_mail(
            'Změna hesla',
            render_to_string('mail/participant_forgotten_password.txt', {
                'token': token.token,
            }),
            settings.EMAIL_SENDER,
            [self.email],
        )

    def get_assignment(self, year):
        try:
            return self.workshops.filter(year=year).first()
        except ObjectDoesNotExist:
            return None
