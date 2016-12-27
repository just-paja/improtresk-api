"""Import Django models."""
from api.models.base import Base

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Text(Base):
    """Stores text types."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=127,
    )
    slug = models.SlugField(
        verbose_name=_("Identifier"),
    )
    text = models.TextField(
        verbose_name=_("Name"),
    )

    class Meta:
        verbose_name = _("Text item")
        verbose_name_plural = _("Text items")

    def __str__(self):
        """Return name as string representation."""
        return self.name
