"""Import Django models."""
from api_textual.models.workshopLocation import WorkshopLocation

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .capacityMixin import CapacityMixin
from .lector import Lector
from .reservation import Reservation
from .workshopDifficulty import WorkshopDifficulty
from .workshopLector import WorkshopLector
from ..fields import VISIBILITY_CHOICES


class Workshop(CapacityMixin, Base):
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
    location = models.ForeignKey(
        WorkshopLocation,
        verbose_name=_("Location"),
    )
    visibility = models.PositiveIntegerField(choices=VISIBILITY_CHOICES)
    lectors = models.ManyToManyField(Lector, related_name='workshops', through=WorkshopLector)

    def get_actual_workshop_price(self, year):
        return self.prices.get(price_level=year.get_actual_price_level())

    def get_reservations_query(self):
        """
        Returns query with reservations associated to self.
        """
        return Reservation.objects.filter(workshop_price__workshop=self)

    def lector_names(self):
        return ", ".join(self.lectors.values_list('name', flat=True))

    def __str__(self):
        """Return name as string representation."""
        return self.name
