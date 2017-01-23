"""Import Django models."""
from django.utils.translation import ugettext_lazy as _

from .abstractText import AbstractText


class Text(AbstractText):
    """Stores Text."""

    class Meta:
        verbose_name = _("Text item")
        verbose_name_plural = _("Text items")
