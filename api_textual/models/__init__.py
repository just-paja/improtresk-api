"""Import all models."""

from .news import News
from .text import Text
from .textPhoto import TextPhoto
from .travelingTip import TravelingTip
from .travelingTipPhoto import TravelingTipPhoto
from .workshopLocation import WorkshopLocation
from .workshopLocationPhoto import WorkshopLocationPhoto

__all__ = (
    News,
    Text,
    TextPhoto,
    TravelingTip,
    TravelingTipPhoto,
    WorkshopLocation,
    WorkshopLocationPhoto,
)
