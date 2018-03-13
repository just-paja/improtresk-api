"""Year model."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .year import Year


class PriceLevel(Base):
    """Stores price levels."""

    year = models.ForeignKey(
        Year,
        verbose_name=_("Year"),
        related_name="price_levels",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=127,
    )
    takes_effect_on = models.DateField(
        verbose_name=_("Date, when this price level takes effect"),
    )
    entryFee = models.PositiveIntegerField(
        default=None,
        blank=True,
        null=True,
        verbose_name=_('Nightly fee'),
    )

    def __str__(self):
        """Return name as string representation."""
        return "%s (%s)" % (self.name, self.year.year)
