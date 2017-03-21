"""Import Django models."""

from api.models.base import Base

from django.db import models


class PollVote(Base):
    """Stores votes for user poll."""

    answer = models.ForeignKey('PollAnswer', related_name='votes')
