"""Year model."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .priceLevel import PriceLevel
from .workshop import Workshop


class WorkshopPrice(Base):
    """Stores worshop price."""

    price_level = models.ForeignKey(
        PriceLevel,
        verbose_name=_("Price level"),
    )
    price = models.PositiveIntegerField(
        verbose_name=_("Price in CZK"),
    )
    workshop = models.ForeignKey(
        Workshop,
        verbose_name=_("Workshop"),
    )

    def __str__(self):
        """Return name as string representation."""
        return "%s - %s (%s,-)" % (self.workshop, self.price_level.name, self.price)
