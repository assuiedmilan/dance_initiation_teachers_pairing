from datetime import datetime
from typing import Dict, Tuple, List

from data.dancer import Dancer
from enumerations.dancer_level import DancerLevel


def match_remaining_beginners(assigned_dates: Dict[datetime, Tuple[str, str]], leads: List[Dancer], follows: List[Dancer]):
    # Get all beginners that were not assigned a date
    unassigned_beginners = [dancer for dancer in (leads + follows) if
                            dancer.level == DancerLevel.BEGINNER and dancer.name not in [name for
                                                                                   date, (lead_name, follow_name) in
                                                                                   assigned_dates.items() for name in
                                                                                   (lead_name, follow_name)]]
    # For each unassigned beginner, attempt to match with an intermediate dancer
    for beginner in unassigned_beginners:
        # Potential intermediate dancers are those who have a common availability date with the beginner, and at least one of their dates is not assigned to a beginner
        potential_intermediates = [dancer for dancer in (leads + follows) if dancer.level == DancerLevel.MEDIUM and any(
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
