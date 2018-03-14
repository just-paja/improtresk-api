"""Signup model."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base


class ParticipantStay(Base):
    """Stores how long participants stay at the festival."""
    participant = models.ForeignKey(
        'Participant',
        verbose_name=_("Participant"),
        related_name='stay',
        on_delete=models.CASCADE,
    )
    date = models.DateField(
        verbose_name=_("Are rules accepted?"),
        help_text=_(
            "Does the participant accepted the rules of the festival?"
        ),
    )
    year = models.ForeignKey(
        'Year',
        verbose_name=_('Year'),
        related_name='stay',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """Return name and status as string representation."""
        return "%s, %s" % (self.participant.name, self.date)
