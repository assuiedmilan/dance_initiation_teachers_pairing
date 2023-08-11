from datetime import datetime
from typing import List

from data.dancer import Dancer


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
            if date in lead.availability and date in follow.availability:
                valid_tuples.append((date, lead, follow))
    return valid_tuples