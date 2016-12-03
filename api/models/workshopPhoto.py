"""Import Django models."""
from django.db import models
from .workshop import Workshop
from .photo import Photo


class WorkshopPhoto(Photo):
    """Stores workshop photos."""

    workshop = models.ForeignKey(Workshop, related_name='photos')
