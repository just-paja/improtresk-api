"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base


class LectorRole(Base):
    """Stores lector roless."""

    class Meta:
        verbose_name = _("Lectors role at workshop")
        verbose_name_plural = _("Lectors roles at workshop")

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=127,
    )
    slug = models.SlugField(
        verbose_name=_("Identifier"),
    )

    def __str__(self):
        """Return name as string representation."""
        return self.name
