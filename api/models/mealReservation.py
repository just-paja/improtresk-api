"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .food import Food
from .meal import Meal
from .reservation import Reservation


class MealReservation(Base):
    """Stores which food was ordered for certain meal."""

    class Meta:
        verbose_name = _("Meal reservation")
        verbose_name_plural = _("Meal reservations")

    food = models.ForeignKey(
        Food,
        verbose_name=_("Food"),
        null=True,
        blank=True,
    )
    meal = models.ForeignKey(
        Meal,
        verbose_name=_("Meal"),
    )
    reservation = models.ForeignKey(
        Reservation,
        verbose_name=_("Reservation"),
    )

    def __str__(self):
        """Return name as string representation."""
        return "Reservation of %s for %s" % (self.food, self.meal)
