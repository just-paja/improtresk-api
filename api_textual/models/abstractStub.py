"""Import Django models."""
from api.models.base import Base
from django.conf import settings

from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractStub(Base):
    """Stores text chapters."""
    text = models.TextField(
        verbose_name=_("Text"),
    )
    lang = models.CharField(
        verbose_name=_('Language'),
        max_length=16,
        choices=settings.LANGUAGES,
        default='cs',
    )

    class Meta:
        verbose_name = _("Text slug")
        verbose_name_plural = _("Text slugs")
        abstract = True
