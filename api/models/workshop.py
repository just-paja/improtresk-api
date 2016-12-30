"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .lector import Lector
from .workshopDifficulty import WorkshopDifficulty
from .workshopLector import WorkshopLector
from ..fields import VISIBILITY_CHOICES


class Workshop(Base):
    """Stores workshops."""

    name = models.CharField(max_length=127)
    desc = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Describe what is the goal of the workshop, props necessary, etc."),
    )
    difficulty = models.ForeignKey(
        WorkshopDifficulty,
        verbose_name=_("Difficulty"),
    )
    visibility = models.PositiveIntegerField(choices=VISIBILITY_CHOICES)
    capacity = models.PositiveIntegerField(
        default=12,
        verbose_name=_("Capacity"),
        help_text=_("How many people can fit in?"),
    )
    lectors = models.ManyToManyField(Lector, related_name='workshops', through=WorkshopLector)

    def __str__(self):
        """Return name as string representation."""
        return self.name
