"""Payment model."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .food import Food
from .meal import Meal
from .order import Order
from .workshopPrice import WorkshopPrice


class Reservation(Base):
    """Stores workshop reservations."""

    workshop_price = models.ForeignKey(
        WorkshopPrice,
        verbose_name=_("Workshop price"),
    )
    order = models.ForeignKey(
        Order,
        verbose_name=_("Order"),
    )
    foods = models.ManyToManyField(
        Food,
        verbose_name=_("Foods"),
        through='MealReservation',
    )
    meals = models.ManyToManyField(
        Meal,
        verbose_name=_("Meals"),
        through='MealReservation',
    )
    ends_at = models.DateTimeField(
        verbose_name=_("Reservation is valid until"),
    )

    def __str__(self):
        """Return name as string representation."""
        return "%s for %s ends at %s" % (
            self.workshop_price.workshop,
            self.workshop_price.price,
            self.ends_at,
        )
