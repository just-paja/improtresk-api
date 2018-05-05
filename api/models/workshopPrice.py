"""Year model."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..fields import format_relation_link

from .base import Base
from .priceLevel import PriceLevel
from .workshop import Workshop


class WorkshopPrice(Base):
    """Stores worshop price."""

    price_level = models.ForeignKey(
        PriceLevel,
        verbose_name=_("Price level"),
        related_name="workshop_prices",
        on_delete=models.PROTECT,
    )
    price = models.PositiveIntegerField(
        verbose_name=_("Price in CZK"),
    )
    workshop = models.ForeignKey(
        Workshop,
        verbose_name=_("Workshop"),
        related_name="prices",
        on_delete=models.CASCADE,
    )

    def price_level_link(self):
        return format_relation_link('api_year', self.price_level.year.id, self.price_level.name)

    def workshop_link(self):
        return format_relation_link('api_workshop', self.workshop.id, self.workshop.name)

    def effective_from(self):
        return self.price_level.takes_effect_on

    def __str__(self):
        """Return name as string representation."""
        return "%s - %s (%s,-)" % (self.workshop, self.price_level.name, self.price)
