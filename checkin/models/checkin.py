"""Year model."""

from django.db import models

from api.models.base import Base


class Checkin(Base):
    """Stores rooms."""
    order = models.ForeignKey(
        'api.Order',
        related_name='rooms',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """Return name as string representation."""
        return "%s %s" % (self.participant.name, self.created_at)
