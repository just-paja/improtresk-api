"""Signup model."""
from django.conf import settings
from django.contrib import auth
from django.core import mail
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from .base import Base
from .participantToken import PASSWORD_RESET, ParticipantToken
from .team import Team
from .workshop import Workshop


class Participant(Base, auth.models.User):
    """Stores participants."""
    USERNAME_FIELD = 'email'

    name = models.CharField(max_length=255)
    address = models.CharField(
        verbose_name=_("Address"),
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
