"""Import Django models."""

from api.models.base import Base

from django.db import models

from django.utils.translation import ugettext_lazy as _


BANDZONE = 'bandzone'
FACEBOOK = 'facebook'
SOUNDCLOUND = 'soundcloud'
YOUTUBE = 'youtube'

SERVICE_CHOICES = (
    (BANDZONE, 'Bandzone'),
    (FACEBOOK, 'Facebook'),
    (SOUNDCLOUND, 'SoundCloud'),
    (YOUTUBE, 'YouTube'),
)


class PerformerLink(Base):
    """Stores Performer Links."""

    performer = models.ForeignKey('Performer', related_name='links')

    name = models.CharField(
        help_text=_("eg. Fish and chips"),
        max_length=127,
        verbose_name=_("Name"),
    )

    service = models.CharField(
        blank=True,
        choices=SERVICE_CHOICES,
        max_length=63,
        null=True,
        verbose_name=_('Linked service'),
    )

    address = models.URLField(
        max_length=255,
        verbose_name=_('URL'),
    )

    def __str__(self):
        """Return name as string representation."""
        return self.name
