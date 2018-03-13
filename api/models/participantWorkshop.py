"""Signup model."""
from django.conf import settings
from django.core import mail
from django.db import models
from django.template.loader import render_to_string

from .base import Base


class ParticipantWorkshop(Base):
    """Stores participants."""
    participant = models.ForeignKey(
        'Participant',
        on_delete=models.CASCADE,
        related_name='workshops',
    )
    workshop = models.ForeignKey(
        'Workshop',
        on_delete=models.PROTECT,
        related_name='participants',
    )
    year = models.ForeignKey(
        'Year',
        on_delete=models.PROTECT,
        related_name='assignments',
        null=True,
    )
    ignore_change = False
    initial_workshop = None

    def __str__(self):
        """Return name and status as string representation."""
        return "%s @ %s" % (self.participant.name, self.workshop.name)

    def __init__(self, *args, **kwargs):
        """Store initial asssignment."""
        super().__init__(*args, **kwargs)
        if self.id and self.workshop_id:
            self.initial_workshop = self.workshop

    def save(self, *args, **kwargs):
        """Save and notify about changes."""
        super().save(*args, **kwargs)
        self.mail_changes()

    def delete(self, *args, **kwargs):
        """Delete assignment and notify about changes."""
        super().delete(*args, *kwargs)
        self.mail_remove()

    def get_reassignment_template(self):
        """Reconcile what e-mail template will be used."""
        template = None

        if not self.initial_workshop and self.workshop:
            template = (
                'Zařazení na workshop',
                'mail/participant_assigned.txt',
            )
        elif (self.initial_workshop and self.workshop and
                self.initial_workshop != self.workshop):
            template = (
                'Přeřazení na jiný workshop',
                'mail/participant_reassigned.txt',
            )

        return template

    def mail_changes(self):
        """E-mail changes to the participant assignment."""
        if self.ignore_change:
            return None

        template = self.get_reassignment_template()

        if not template:
            return None

        body = render_to_string(template, {
            'prevWorkshop': self.initial_workshop,
            'currentWorkshop': self.workshop,
        })
        mail.send_mail(template[0], body, settings.EMAIL_SENDER, [self.participant.email])

    def mail_remove(self):
        """E-mail changes to the participant assignment."""
        if self.ignore_change:
            return None
        body = render_to_string('mail/participant_removed.txt', {
            'prevWorkshop': self.workshop,
        })
        mail.send_mail(
            'Odhlášení z workshopu',
            body,
            settings.EMAIL_SENDER,
            [self.participant.email]
        )
