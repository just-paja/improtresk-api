"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .abstractText import AbstractText


class WorkshopLocation(AbstractText):
    """Stores workshop location."""

    address = models.TextField(
        verbose_name=_("Address"),
    )

    class Meta:
        verbose_name = _("Workshop location")
        verbose_name_plural = _("Workshop locations")
