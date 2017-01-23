"""Import Django models."""
from django.db import models

from .lector import Lector
from .photo import Photo


class LectorPhoto(Photo):
    """Stores lector photos."""

    lector = models.ForeignKey(Lector, related_name='photos')
