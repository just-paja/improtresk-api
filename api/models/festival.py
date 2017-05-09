"""Festival model."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base


class Festival(Base):
    """Stores festivals."""

    name = models.CharField(
        verbose_name=_("Festival name"),
        max_length=255,
        unique=True,
    )
    discontinued = models.BooleanField(
        verbose_name=_('Discontinued'),
        help_text=_('Was festival discontinued'),
        default=False,
    )

    def __str__(self):
        """Return name as string representation."""
        return "Festival %s" % self.name
