"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from ..fields import VISIBILITY_CHOICES, VISIBILITY_PUBLIC


class Team(Base):
    """Stores teams."""

    name = models.CharField(
        verbose_name=_("Team name"),
        max_length=127,
        unique=True,
        blank=True,
    )
    desc = models.TextField(
        verbose_name=_("Team description"),
        null=True,
        blank=True,
    )
    visibility = models.PositiveIntegerField(
        verbose_name=_("Visibility"),
        default=VISIBILITY_PUBLIC,
        choices=VISIBILITY_CHOICES,
    )

    def __str__(self):
        """Return name as string representation."""
        return self.name
