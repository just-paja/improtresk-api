"""Rule model."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base
from .year import Year


class Rules(Base):
    """Stores rules, terms and conditions for year."""

    year = models.ForeignKey(
        Year,
        verbose_name=_("Year"),
    )
    text = models.TextField(
        verbose_name=_("Rules, terms and conditions"),
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = _("Rules, terms and conditions")
        verbose_name_plural = _("Rules, terms and conditions")

    def __str__(self):
        """Return created at as string representation."""
        return "%s (%s)" % (_("Rules"), self.createdAt)