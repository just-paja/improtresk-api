"""Tokens for participants."""

import uuid

from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .base import Base

PASSWORD_RESET = 'password-reset'
EMAIL_CONFIRM = 'email-confirm'

TOKEN_TYPE_CHOICES = (
    (PASSWORD_RESET, _('Password reset')),
    (EMAIL_CONFIRM, _('E-mail confirmation')),
)


class ParticipantToken(Base):
    """Stores one time access tokens for participants."""

    participant = models.ForeignKey(
        'Participant',
        verbose_name=_('Participant'),
        related_name='tokens',
        on_delete=models.CASCADE,
    )
    token = models.CharField(
        max_length=255,
        verbose_name=_('Token'),
    )
    token_type = models.CharField(
        max_length=31,
        verbose_name=_('Token type'),
        choices=TOKEN_TYPE_CHOICES,
    )
    valid_until = models.DateTimeField(
        verbose_name=_('Expiration date'),
    )
    used = models.BooleanField(
        default=False,
        verbose_name=_("Was token already used?"),
    )

    def __str__(self):
        """Return participant name, expiry date and type and validness."""
        return "%s: %s, (%s)" % (
            self.participant.name,
            self.get_token_type_display(),
            self.valid_until if self.is_valid() else 'expired'
        )

    def is_valid(self):
        return self.valid_until < datetime.now(timezone.get_current_timezone())

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4()
            self.valid_until = datetime.now(timezone.get_current_timezone())\
                + timedelta(days=2)
        return super().save(*args, **kwargs)
