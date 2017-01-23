"""Import Django models."""
from django.db import models

from .photo import Photo
from .workshop import Workshop


class WorkshopPhoto(Photo):
    """Stores workshop photos."""

    workshop = models.ForeignKey(Workshop, related_name='photos')
