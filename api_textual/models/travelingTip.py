"""Import Django models."""
from django.utils.translation import ugettext_lazy as _

from .abstractText import AbstractText


class TravelingTip(AbstractText):
    """Stores traveling tips."""

    class Meta:
        verbose_name = _("Traveling tip")
        verbose_name_plural = _("Traveling tips")
