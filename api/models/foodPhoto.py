"""Import Django models."""
from django.db import models

from .food import Food
from .photo import Photo


class FoodPhoto(Photo):
    """Stores accomodation photos."""

    food = models.ForeignKey(Food, related_name='photos')
