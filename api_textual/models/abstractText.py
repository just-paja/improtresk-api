"""Import Django models."""
from api.models.base import Base

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_markdown.models import MarkdownField


class AbstractText(Base):
    """Stores text types."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=127,
    )
    slug = models.SlugField(
        verbose_name=_("Identifier in URL"),
    )
    text = MarkdownField(
        verbose_name=_("Text"),
    )

    class Meta:
        verbose_name = _("Text item")
        verbose_name_plural = _("Text items")

        abstract = True

    def __str__(self):
        """Return name as string representation."""
        return self.name
