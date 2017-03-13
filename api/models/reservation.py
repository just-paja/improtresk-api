"""Payment model."""
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .base import Base


class Reservation(Base):
    """Stores workshop reservations."""

    workshop_price = models.ForeignKey(
        'WorkshopPrice',
        verbose_name=_("Workshop price"),
    )
    order = models.OneToOneField(
        'Order',
        verbose_name=_("Order"),
        related_name="reservation",
    )
    foods = models.ManyToManyField(
        'Food',
        verbose_name=_("Foods"),
        through='MealReservation',
    )
    meals = models.ManyToManyField(
        'Meal',
        verbose_name=_("Meals"),
        through='MealReservation',
    )
    accomodation = models.ForeignKey(
        'Accomodation',
        verbose_name=_("Accomodation"),
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

    def save(self, *args, **kwargs):
        """Set ends_at field."""
        if not self.ends_at:
            self.ends_at = timezone.now() + settings.RESERVATION_DURATION_SHORT
        super().save(*args, **kwargs)

    def extend_reservation(self):
        """ Payment was created, extend validity of this reservation """
        if self.ends_at >= timezone.now():
            self.ends_at = timezone.now() + settings.RESERVATION_DURATION_PAYMENT
