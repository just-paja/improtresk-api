"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from ..fields import VISIBILITY_CHOICES


class Accomodation(Base):
    """Stores accomodation types."""

    name = models.CharField(
        verbose_name=_("Accomodation name"),
        help_text=_("eg. Hotel Stadion"),
        max_length=127
    )
    desc = models.TextField(
        verbose_name=_("Description formatted in Markdown"),
        help_text=_("eg. Describe room, location, type of accomodation"),
    )
    price = models.PositiveIntegerField(
        verbose_name=_("Price"),
        help_text=_("Price per night in CZK"),
    )
    visibility = models.PositiveIntegerField(choices=VISIBILITY_CHOICES)
    capacity = models.PositiveIntegerField(
        default=12,
        verbose_name=_("Capacity"),
        help_text=_("How many people can fit in"),
    )

    def __str__(self):
        """Return name as string representation."""
        return self.name
