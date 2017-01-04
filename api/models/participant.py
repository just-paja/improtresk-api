"""Signup model."""
from django.conf import settings
from django.contrib import auth
from django.core import mail
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..mail import signup as templates
from ..mail.common import formatMail, formatWorkshop
from .base import Base
from .team import Team
from .workshop import Workshop


class Participant(Base, auth.models.AbstractBaseUser):
    """Stores participants."""

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
    )
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    birthday = models.DateField(
        verbose_name=_("Date of birthday"),
    )

    rules = models.BooleanField(default=False)
    newsletter = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    assigned_workshop = models.ForeignKey(Workshop, blank=True, null=True)

    def __str__(self):
        """Return name and status as string representation."""
        status = 'assigned' if self.assigned_workshop else 'unassigned'
        return "%s (%s)" % (self.name, status)

    def __init__(self, *args, **kwargs):
        """Store initial asssignment."""
        super().__init__(*args, **kwargs)
        self.initialAssignment = self.assigned_workshop

    def save(self, *args, **kwargs):
        """Save and notify about changes."""
        super().save(*args, **kwargs)
        self.mailReassignment()

    def getReassignmentTemplate(self):
        """Reconcile what e-mail template will be used."""
        template = None

        if not self.initialAssignment and self.assigned_workshop:
            template = (
                templates.ASSIGNED_SUBJECT,
                templates.ASSIGNED_BODY,
            )
        elif self.initialAssignment and not self.assigned_workshop:
            template = (
                templates.REMOVED_SUBJECT,
                templates.REMOVED_BODY,
            )
        elif (self.initialAssignment and self.assigned_workshop and
                self.initialAssignment != self.assigned_workshop):
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
                'lectorName': self.initialAssignment.lector.name,
            })

        if self.assigned_workshop:
            currentWorkshop = formatWorkshop({
                'name': self.assigned_workshop.name,
                'lectorName': self.assigned_workshop.lector.name,
            })

        return formatMail(template, {
            'prevWorkshop': prevWorkshop,
            'currentWorkshop': currentWorkshop,
            'workshopPreferences': 'foo',
        })

    def mailReassignment(self):
        """E-mail changes to the participant assignment."""
        template = self.getReassignmentTemplate()

        if not template:
            return None

        body = self.getReassignmentMailBody(template[1])
        mail.send_mail(template[0], body, settings.EMAIL_SENDER, [self.email])
