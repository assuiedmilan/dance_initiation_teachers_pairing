import random
from collections import defaultdict
from datetime import datetime
from typing import Tuple, List, Dict

from data.dancer import Dancer


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

