from resolver.balance_performances import balance_performances
from resolver.generate_tuples import generate_tuples, filter_valid_tuples
from resolver.match_begginers import match_remaining_beginners


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