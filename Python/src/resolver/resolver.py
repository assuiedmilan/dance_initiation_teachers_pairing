import random

from enum import Enum
from datetime import datetime
from typing import Dict, List, Tuple
from collections import defaultdict
from itertools import chain

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

    def __eq__(self, other):
        if not isinstance(other, Dancer):
            return NotImplemented
        return self.name == other.name and self.level == other.level and self.is_lead == other.is_lead

    def __hash__(self):
        return hash((self.name, self.level, self.is_lead))

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


def balance_performances(valid_tuples: List[Tuple[datetime, Dancer, Dancer]]) -> Dict[datetime, Tuple[str, str]]:
    # Count the number of performances for each dancer
    performance_count = defaultdict(int)
    final_match = {}

    for date, lead, follow in valid_tuples:
        performance_count[lead.name] += 1
        performance_count[follow.name] += 1

    # Sorting valid_tuples based on the total performances of both dancers and their experience level
    valid_tuples.sort(
        key=lambda x: (
            performance_count[x[1].name],
            performance_count[x[2].name],
            max(x[1].level.value, x[2].level.value)
        )
    )

    # Grouping valid tuples by date
    date_tuples = defaultdict(list)
    for date, lead, follow in valid_tuples:
        date_tuples[date].append((lead, follow))

    # Assign performances based on balance and experience level
    for date, tuples in date_tuples.items():
        if len(tuples) == 1:
            final_match[date] = (tuples[0][0].name, tuples[0][1].name)
        else:
            # Select the tuple with less total performances and lower experience level
            min_performances = min(performance_count[possible_pair[0].name] + performance_count[possible_pair[1].name] for possible_pair in tuples)
            potential_tuples = [t for t in tuples if performance_count[t[0].name] + performance_count[t[1].name] == min_performances]

            if len(potential_tuples) > 1:
                # Select randomly among tuples with zero performances
                zero_performances_tuples = [t for t in potential_tuples if performance_count[t[0].name] + performance_count[t[1].name] == 0]
                if zero_performances_tuples:
                    chosen_tuple = random.choice(zero_performances_tuples)
                else:
                    # Select the tuple with lower experience level
                    min_level = min(max(t[0].level.value, t[1].level.value) for t in potential_tuples)
                    chosen_tuple = next(t for t in potential_tuples if max(t[0].level.value, t[1].level.value) == min_level)
            else:
                chosen_tuple = potential_tuples[0]

            final_match[date] = (chosen_tuple[0].name, chosen_tuple[1].name)

    return final_match


def match_remaining_beginners(assigned_dates: Dict[datetime, Tuple[str, str]], leads: List[Dancer],
                              follows: List[Dancer]):
    # Get all beginners that were not assigned a date
    unassigned_beginners = [dancer for dancer in (leads + follows) if
                            dancer.level == Level.BEGINNER and dancer.name not in [name for
                                                                                   date, (lead_name, follow_name) in
                                                                                   assigned_dates.items() for name in
                                                                                   (lead_name, follow_name)]]
    # For each unassigned beginner, attempt to match with an intermediate dancer
    for beginner in unassigned_beginners:
        # Potential intermediate dancers are those who have a common availability date with the beginner, and at least one of their dates is not assigned to a beginner
        potential_intermediates = [dancer for dancer in (leads + follows) if dancer.level == Level.MEDIUM and any(
            date in beginner.availability for date in dancer.availability) and any(
            date not in [date for date, (lead_name, follow_name) in assigned_dates.items() if
                         beginner.name in (lead_name, follow_name)] for date in dancer.availability)]
        # Sort potential intermediates by their number of assigned dates
        potential_intermediates.sort(key=lambda dancer: len(
            [date for date, (lead_name, follow_name) in assigned_dates.items() if
             dancer.name in (lead_name, follow_name)]))
        # Select the intermediate dancer with the fewest assigned dates
        if potential_intermediates:
            intermediate = potential_intermediates[0]
            common_dates = list(set(beginner.availability) & set(intermediate.availability))
            common_dates.sort(key=lambda date: len(
                [dancer_name for date_, (lead_name, follow_name) in assigned_dates.items() if date_ == date for
                 dancer_name in (lead_name, follow_name)]))
            if common_dates:
                selected_date = common_dates[0]
                if beginner.is_lead:
                    assigned_dates[selected_date] = (beginner.name, intermediate.name)
                else:
                    assigned_dates[selected_date] = (intermediate.name, beginner.name)

    return assigned_dates



def assign_dates(leads, follows, dates):
    possible_tuples = []
    for lead in leads:
        possible_tuples.extend(generate_tuples(lead, follows, dates))
    valid_tuples = filter_valid_tuples(possible_tuples)

    final_match = balance_performances(valid_tuples)
    final_match = match_remaining_beginners(final_match, leads, follows)

    for date in dates:
        if date not in final_match:
            final_match[date] = ('No match', 'No match')

    return dict(sorted(final_match.items()))
