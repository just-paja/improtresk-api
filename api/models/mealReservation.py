"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ..fields import format_relation_link, format_checkin_link

from .base import Base


class MealReservation(Base):
    """Stores which food was ordered for certain meal."""

    class Meta:
        verbose_name = _("Meal reservation")
        verbose_name_plural = _("Meal reservations")

    food = models.ForeignKey(
        'Food',
        verbose_name=_("Food"),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    soup = models.ForeignKey(
        'Soup',
        verbose_name=_("Soup"),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    meal = models.ForeignKey(
        'Meal',
        verbose_name=_("Meal"),
        on_delete=models.PROTECT,
    )
    reservation = models.ForeignKey(
        'Reservation',
        verbose_name=_("Reservation"),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """Return name as string representation."""
        food_name = self.food.name if self.food else None
        soup_name = self.soup.name if self.soup else None
        return "Reservation of %s and %s for %s" % (food_name, soup_name, self.meal)

    def participant_link(self):
        return format_relation_link(
            'api_participant',
            self.reservation.order.participant.id,
            self.reservation.order.participant
        )

    def order_link(self):
        return format_relation_link(
            'api_order',
            self.reservation.order.id,
            self.reservation.order.id
        )

    def reservation_link(self):
        return format_relation_link(
            'api_reservation',
            self.reservation.id,
            self.reservation.id
        )

    def checkin_link(self):
        return format_checkin_link(self.reservation.order.get_code())
