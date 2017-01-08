"""Import Django models."""
from api.models.photo import Photo

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .travelingTip import TravelingTip


class TravelingTipPhoto(Photo):
    """Stores traveling tip photos."""

    text = models.ForeignKey(
        TravelingTip,
        verbose_name=_("Traveling tip"),
        related_name='photos',
    )
