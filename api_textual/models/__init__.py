"""Import all models."""

from .news import News
from .newsPhoto import NewsPhoto
from .performer import Performer
from .performerPhoto import PerformerPhoto
from .text import Text
from .textPhoto import TextPhoto
from .travelingTip import TravelingTip
from .travelingTipPhoto import TravelingTipPhoto
from .workshopLocation import WorkshopLocation
from .workshopLocationPhoto import WorkshopLocationPhoto

__all__ = (
    News,
    NewsPhoto,
    Performer,
    PerformerPhoto,
    Text,
    TextPhoto,
    TravelingTip,
    TravelingTipPhoto,
    WorkshopLocation,
    WorkshopLocationPhoto,
)
