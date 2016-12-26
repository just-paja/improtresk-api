"""Import Django models."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import Base


class WorkshopDifficulty(Base):
    """Stores workshop photos."""

    class Meta:
        verbose_name = _("Workshop difficulty")
        verbose_name_plural = _("Workshop difficulties")

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
    )
    slug = models.SlugField(
        verbose_name=_("Identifier"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
    )

    def __str__(self):
        """Return name as string representation."""
        return self.name
