from enumerations.dancer_level import DancerLevel
from typing import List

from datetime import datetime

class Dancer:
    def __init__(self, name: str, level: DancerLevel, is_lead: bool):
        self.name = name
        self.level = level
        self.is_lead = is_lead
        self.availability = []
        self.performed_dates = []

    def add_availability(self, dates: List[datetime]):
        self.availability.extend(dates)

    def can_match(self, other):
        if self.level == DancerLevel.BEGINNER and other.level != DancerLevel.EXPERT:
            return False
        if other.level == DancerLevel.BEGINNER and self.level != DancerLevel.EXPERT:
            return False
        return True

    @property
    def performances(self):
        return len(self.performed_dates)

    def __eq__(self, other):
        if not isinstance(other, Dancer):
            return NotImplemented
        return self.name == other.name and self.level == other.level and self.is_lead == other.is_lead

    def __hash__(self):
        return hash((self.name, self.level, self.is_lead))
