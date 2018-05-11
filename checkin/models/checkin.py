"""Year model."""

from api.fields import format_relation_link
from django.conf import settings
from django.core import mail
from django.db import models
from django.template.loader import render_to_string

from api.models.base import Base


class Checkin(Base):
    """Stores rooms."""
    order = models.ForeignKey(
        'api.Order',
        related_name='rooms',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """Return name as string representation."""
        return "%s %s" % (self.order.participant.name, self.created_at)

    def participant_link(self):
        return format_relation_link(
            'api_participant',
            self.order.participant.id,
            self.order.participant
        )

    def save(self, *args, **kwargs):
        if not self.id:
            self.mail_welcome()
        super().save(*args, **kwargs)

    def mail_welcome(self):
        mail.send_mail(
            'Vítej na Improtřesku',
            render_to_string('mail/welcome.txt'),
            settings.EMAIL_SENDER,
            [self.order.participant.email],
        )

    participant_link.short_description = "Participant"
