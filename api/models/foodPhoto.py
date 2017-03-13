"""Import Django models."""
from django.db import models

from .food import AbstractFood
from .photo import Photo


class FoodPhoto(Photo):
    """Stores accomodation photos."""

    food = models.ForeignKey(AbstractFood, related_name='photos')
