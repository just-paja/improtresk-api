"""Base model class."""
import datetime

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


class CapacityMixin(models.Model):
    """Mixin, that adds a capacity field and ensures that capacity is not exceeded"""

    capacity = models.PositiveIntegerField(
        verbose_name=_("Capacity"),
        help_text=_("How many people can fit in"),
        blank=True,
        null=True,
    )

    def get_reservations_query(self):
        """
        Returns query with reservations associated to self.
        """
        return NotImplemented

    def number_of_reservations(self):
        """
        Returns number of reservations to this objet.
        """
        return self.get_reservations_query().filter(
            Q(order__paid=True) | Q(ends_at__gt=datetime.datetime.now()),
        ).distinct().count()

    def has_free_capacity(self):
        """ Returns if the object has still a free capacity and other reservations can be add. """
        if self.capacity:
            return self.number_of_reservations() < self.capacity
        return True

    class Meta:
        """Makes the model abstract."""

        abstract = True
