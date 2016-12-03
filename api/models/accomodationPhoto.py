"""Import Django models."""
from django.db import models
from .accomodation import Accomodation
from .photo import Photo


class AccomodationPhoto(Photo):
    """Stores accomodation photos."""

    accomodation = models.ForeignKey(Accomodation, related_name='photos')
