"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from api.models.base import Base

class WorkshopLocation(Base):
    """Stores workshop location."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=127,
    )
    slug = models.SlugField(
        verbose_name=_("Identifier in URL"),
    )
    address = models.TextField(
        verbose_name=_("Address"),
    )

    class Meta:
        verbose_name = _("Workshop location")
        verbose_name_plural = _("Workshop locations")
