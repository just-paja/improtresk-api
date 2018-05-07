"""Year model."""

from api.fields import format_relation_link
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
        return "%s %s" % (self.order.participant.name, self.created_at)

    def participant_link(self):
        return format_relation_link(
            'api_participant',
            self.order.participant.id,
            self.order.participant
        )

    participant_link.short_description = "Participant"
