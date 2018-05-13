"""Import all models."""

from .accomodation_inhabitant_list import accomodation_inhabitant_list
from .allowance_list import allowance_list
from .food_delivery import food_delivery
from .food_stats import food_stats
from .index import index
from .numbers import numbers
from .participant_list import participant_list
from .participant_teams import participant_teams
from .workshop_attendance import workshop_attendance
from .workshop_capacity import workshop_capacity
from .workshop_participants import workshop_participants

__all__ = (
    accomodation_inhabitant_list,
    allowance_list,
    food_delivery,
    food_stats,
    index,
    numbers,
    participant_list,
    participant_teams,
    workshop_attendance,
    workshop_capacity,
    workshop_participants,
)
