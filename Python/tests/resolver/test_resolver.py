import pytest
from datetime import datetime

from resolver.resolver import Dancer, Level, filter_valid_tuples, generate_tuples, assign_dates


# Use the classes and functions defined above

def test_generate_tuples():
    dates = [datetime(2023, 7, i) for i in range(1, 7)]
    john = Dancer('John', Level.EXPERT, True)
    john.add_availability(dates)
    jane = Dancer('Jane', Level.MEDIUM, False)
    jane.add_availability(dates)
    tuples = generate_tuples(john, [jane], dates)
    assert len(tuples) == 6  # All dates should have a match

    jane.add_availability([datetime(2023, 7, 7)])
    tuples = generate_tuples(john, [jane], dates)
    assert len(tuples) == 6  # Extra availability shouldn't create extra matches

    jane = Dancer('Jane', Level.MEDIUM, False)  # New Jane with no availability
    tuples = generate_tuples(john, [jane], dates)
    assert len(tuples) == 0  # No match should be found

@pytest.mark.parametrize("lead_level,follow_level", [(Level.BEGINNER, Level.EXPERT),
                                                     (Level.MEDIUM, Level.EXPERT),
                                                     (Level.EXPERT, Level.EXPERT),
                                                     (Level.EXPERT, Level.BEGINNER),
                                                     (Level.EXPERT, Level.MEDIUM)])
def test_filter_valid_tuples_allow(lead_level, follow_level):
    dates = [datetime(2023, 7, 1)]
    john = Dancer('John', lead_level, True)
    john.add_availability(dates)
    jane = Dancer('Jane', follow_level, False)
    jane.add_availability(dates)
    tuples = [(dates[0], john, jane)]
    valid_tuples = filter_valid_tuples(tuples)
    assert len(valid_tuples) == 1  # This pair should be allowed

@pytest.mark.parametrize("lead_level,follow_level", [(Level.BEGINNER, Level.MEDIUM),
                                                     (Level.MEDIUM, Level.BEGINNER)])
def test_filter_valid_tuples_not_allow(lead_level, follow_level):
    dates = [datetime(2023, 7, 1)]
    john = Dancer('John', lead_level, True)
    john.add_availability(dates)
    jane = Dancer('Jane', follow_level, False)
    jane.add_availability(dates)
    tuples = [(dates[0], john, jane)]
    valid_tuples = filter_valid_tuples(tuples)
    assert len(valid_tuples) == 0  # This pair should not be allowed


def test_filter_valid_tuples_no_common_availability():
    dates = [datetime(2023, 7, 1)]
    john = Dancer('John', Level.EXPERT, True)
    john.add_availability(dates)
    jane = Dancer('Jane', Level.BEGINNER, False)
    jane.add_availability([datetime(2023, 7, 2)])
    tuples = [(dates[0], john, jane)]
    valid_tuples = filter_valid_tuples(tuples)
    assert len(valid_tuples) == 0  # This pair should not be allowed

def test_assign_dates():
    dates = [datetime(2023, 7, i) for i in range(1, 7)]
    leads = [Dancer(f'Lead {i}', Level.EXPERT, True) for i in range(1, 7)]
    follows = [Dancer(f'Follow {i}', Level.MEDIUM, False) for i in range(1, 5)]

    for i, lead in enumerate(leads):
        lead.add_availability(dates[:i+1])  # Each lead is available on i+1 dates

    for follow in follows:
        follow.add_availability(dates)  # Each follow is available on all dates

    final_match = assign_dates(leads, follows, dates)

    assert len(final_match) == len(dates)  # All dates should have a match

    for match in final_match.values():
        assert match != ('No match', 'No match')  # All matches should be valid