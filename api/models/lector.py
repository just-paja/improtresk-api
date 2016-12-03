"""Import Django models."""
from django.db import models
from .base import Base


class Lector(Base):
    """Stores lectors."""

    name = models.CharField(max_length=127)
    about = models.TextField()
