"""Signup model."""
from django.conf import settings
from django.core import mail
from django.db import models

from .base import Base
from ..mail import signup as templates
from ..mail.common import formatMail, formatWorkshop


class ParticipantWorkshop(Base):
    """Stores participants."""
    participant = models.ForeignKey(
        'Participant',
        on_delete=models.CASCADE,
    )
    workshop = models.ForeignKey(
        'Workshop',
        on_delete=models.PROTECT,
    )
    ignore_change = False

    def __str__(self):
        """Return name and status as string representation."""
        return "%s @ %s" % (self.participant.name, self.workshop.name)

    def __init__(self, *args, **kwargs):
        """Store initial asssignment."""
        super().__init__(*args, **kwargs)
        if self.workshop_id:
            self.initialAssignment = self.workshop

    def save(self, *args, **kwargs):
        """Save and notify about changes."""
        super().save(*args, **kwargs)
        self.mailReassignment()

    def getReassignmentTemplate(self):
        """Reconcile what e-mail template will be used."""
        template = None

        if not self.initialAssignment and self.workshop:
            template = (
                templates.ASSIGNED_SUBJECT,
                templates.ASSIGNED_BODY,
            )
        elif self.initialAssignment and not self.workshop:
            template = (
                templates.REMOVED_SUBJECT,
                templates.REMOVED_BODY,
            )
        elif (self.initialAssignment and self.workshop and
                self.initialAssignment != self.workshop):
            template = (
                templates.REASSIGNED_SUBJECT,
                templates.REASSIGNED_BODY,
            )

        return template

    def getReassignmentMailBody(self, template):
        """Format template body to be emailed."""
        prevWorkshop = None
        currentWorkshop = None

        if self.initialAssignment:
            prevWorkshop = formatWorkshop({
                'name': self.initialAssignment.name,
                'lectorName': self.initialAssignment.lector_names(),
            })

        if self.workshop:
            currentWorkshop = formatWorkshop({
                'name': self.workshop.name,
                'lectorName': self.workshop.lector_names(),
            })

        return formatMail(
            template,
            {
                'prevWorkshop': prevWorkshop,
                'currentWorkshop': currentWorkshop,
                'workshopPreferences': 'foo',
            },
        )

    def mailReassignment(self):
        """E-mail changes to the participant assignment."""
        if self.ignore_change:
            return None

        template = self.getReassignmentTemplate()

        if not template:
            return None

        body = self.getReassignmentMailBody(template[1])
        mail.send_mail(template[0], body, settings.EMAIL_SENDER, [self.participant.email])
