from enum import Enum
from collections import defaultdict
from typing import List
from datetime import datetime


class Level(Enum):
    EXPERT = 3
    MEDIUM = 2
    BEGINNER = 1


class Dancer:
    def __init__(self, name: str, level: Level, is_lead: bool):
        self.name = name
        self.level = level
        self.is_lead = is_lead
        self.availability = []
        self.performed_dates = []

    def add_availability(self, dates: List[datetime]):
        self.availability.extend(dates)

    def can_match(self, other):
        if self.level == Level.BEGINNER and other.level != Level.EXPERT:
            return False
        if other.level == Level.BEGINNER and self.level != Level.EXPERT:
            return False
        return True

    @property
    def performances(self):
        return len(self.performed_dates)


def generate_tuples(lead: Dancer, follows: List[Dancer], dates: List[datetime]):
    possible_matches = []
    for date in dates:
        if date in lead.availability:
            for follow in follows:
                if date in follow.availability:
                    possible_matches.append((date, lead, follow))
    return possible_matches


def filter_valid_tuples(tuples):
    valid_tuples = []
    for date, lead, follow in tuples:
        if lead.can_match(follow) and follow.can_match(lead):
            valid_tuples.append((date, lead, follow))
    return valid_tuples


def balance_performances(valid_tuples):
    date_to_match = defaultdict(list)
    for date, lead, follow in valid_tuples:
        date_to_match[date].append((lead, follow))

    final_match = {}
    for date, tuples in date_to_match.items():
        tuples.sort(key=lambda x: abs(x[0].performances - x[1].performances))
        lead, follow = tuples[0]
        final_match[date] = (lead.name, follow.name)
        lead.performed_dates.append(date)
        follow.performed_dates.append(date)

    return final_match


def assign_dates(leads, follows, dates):
    possible_tuples = []
    for lead in leads:
        possible_tuples.extend(generate_tuples(lead, follows, dates))
    valid_tuples = filter_valid_tuples(possible_tuples)
    final_match = balance_performances(valid_tuples)
    for date in dates:
        if date not in final_match:
            final_match[date] = ('No match', 'No match')
    return final_match
