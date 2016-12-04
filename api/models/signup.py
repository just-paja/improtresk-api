"""Signup model."""
from django.conf import settings
from django.core import mail
from django.db import models

from ..mail import signup as templates
from ..mail.common import formatMail, formatWorkshop
from .base import Base
from .workshop import Workshop


class Signup(Base):
    """Stores signups."""

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    team = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255)

    rules = models.BooleanField(default=False)
    newsletter = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    assignedWorkshop = models.ForeignKey(Workshop, blank=True, null=True)

    def __str__(self):
        """Return name and status as string representation."""
        status = 'assigned' if self.assignedWorkshop else 'unassigned'
        return "%s (%s)" % (self.name, status)

    def __init__(self, *args, **kwargs):
        """Store initial asssignment."""
        super(Signup, self).__init__(*args, **kwargs)
        self.initialAssignment = self.assignedWorkshop

    def save(self, *args, **kwargs):
        """Save and notify about changes."""
        super(Signup, self).save(*args, **kwargs)
        self.mailReassignment()

    def getReassignmentTemplate(self):
        """Reconcile what e-mail template will be used."""
        template = None

        if not self.initialAssignment and self.assignedWorkshop:
            template = (
                templates.ASSIGNED_SUBJECT,
                templates.ASSIGNED_BODY,
            )
        elif self.initialAssignment and not self.assignedWorkshop:
            template = (
                templates.REMOVED_SUBJECT,
                templates.REMOVED_BODY,
            )
        elif (self.initialAssignment and self.assignedWorkshop and
                self.initialAssignment != self.assignedWorkshop):
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

        if self.assignedWorkshop:
            currentWorkshop = formatWorkshop({
                'name': self.assignedWorkshop.name,
                'lectorName': self.assignedWorkshop.lector.name,
            })

        return formatMail(template, {
            'prevWorkshop': prevWorkshop,
            'currentWorkshop': currentWorkshop,
            'workshopPreferences': 'foo',
        })

    def mailReassignment(self):
        """E-mail changes to the signup assignment."""
        template = self.getReassignmentTemplate()

        if not template:
            return None

        body = self.getReassignmentMailBody(template[1])
        mail.send_mail(template[0], body, settings.EMAIL_SENDER, [self.email])
