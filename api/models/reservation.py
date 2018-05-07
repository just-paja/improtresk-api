"""Payment model."""
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .base import Base
from ..fields import format_relation_link, format_checkin_link


class Reservation(Base):
    """Stores workshop reservations."""

    workshop_price = models.ForeignKey(
        'WorkshopPrice',
        verbose_name=_("Workshop price"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    order = models.OneToOneField(
        'Order',
        verbose_name=_("Order"),
        related_name="reservation",
        on_delete=models.CASCADE,
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
        on_delete=models.PROTECT,
    )
    ends_at = models.DateTimeField(
        verbose_name=_("Reservation is valid until"),
    )

    def workshop(self):
        return self.workshop_price.workshop if self.workshop_price else None

    def participant(self):
        return self.order.participant

    def get_meals_price(self):
        return self.meals.aggregate(
            total=models.functions.Coalesce(
                models.Sum('mealreservation__meal__price'),
                0,
            ),
        ).get('total')

    def get_workshop_price(self):
        return self.workshop_price.price if self.workshop_price else 0

    def get_stay_price(self):
        if not self.workshop_price:
            price_level = None
            year = self.order.year
            if year:
                stay_length = self.order.participant.stay.filter(year=year).count()
                price_level = year.get_actual_price_level()

            if price_level and price_level.entryFee:
                return price_level.entryFee * stay_length

        return 0

    def get_workshop_name(self):
        return self.workshop().name if self.workshop() else None

    def price(self):
        return self.get_workshop_price() + self.get_meals_price() + self.get_stay_price()

    def is_valid(self):
        if self.order and self.order.paid:
            return True
        if self.ends_at:
            return timezone.now() < self.ends_at and not self.order.canceled
        return False

    is_valid.boolean = True

    def __str__(self):
        """Return name as string representation."""
        return "%s for %s ends at %s" % (
            self.get_workshop_name(),
            self.price(),
            self.ends_at,
        )

    def save(self, *args, **kwargs):
        """Set ends_at field."""
        if not self.ends_at:
            self.ends_at = timezone.now() + settings.RESERVATION_DURATION_SHORT

        super().save(*args, **kwargs)
        self.update_price()

    def update_price(self):
        price = self.price()
        if self.order and not self.order.paid and self.order.price != price:
            self.order.price = price
            if self.order.confirmed and not self.order.canceled:
                self.order.update_paid_status()
            else:
                self.order.save()

    def extend_reservation(self):
        """ Payment was created, extend validity of this reservation """
        if self.ends_at >= timezone.now():
            self.ends_at = (
                timezone.now() +
                settings.RESERVATION_DURATION_PAYMENT
            )

    def order_link(self):
        return format_relation_link('api_order', self.order.id, self.order.symvar)

    def participant_link(self):
        return format_relation_link(
            'api_participant',
            self.order.participant.id,
            self.order.participant,
        )

    def checkin_link(self):
        return format_checkin_link(self.order.get_code())

    order_link.short_description = "Order"
    participant_link.short_description = "Participant"
