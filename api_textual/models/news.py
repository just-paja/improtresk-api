"""Import Django models."""
from django.utils.translation import ugettext_lazy as _

from .abstractText import AbstractText


class News(AbstractText):
    """Stores news."""

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News list")
