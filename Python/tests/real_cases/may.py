from datetime import datetime

from resolver.resolver import Dancer, Level, assign_dates

jean_yves = Dancer("JY", Level.EXPERT, is_lead=True)
erik = Dancer("Erik", Level.BEGINNER, is_lead=True)
baptiste = Dancer("Baptiste", Level.MEDIUM, is_lead=True)
nicolas = Dancer("Nicolas", Level.MEDIUM, is_lead=True)
mathieu = Dancer("Mathieu", Level.MEDIUM, is_lead=True)
ulukai = Dancer("Ulukai", Level.BEGINNER, is_lead=True)

lea = Dancer("Lea", Level.EXPERT, is_lead=False)
veronique = Dancer("Veronique", Level.EXPERT, is_lead=False)
natasha = Dancer("Natasha", Level.BEGINNER, is_lead=False)
caroline = Dancer("Caroline", Level.BEGINNER, is_lead=False)

jean_yves.add_availability([datetime(2023, 5, 2), datetime(2023, 5, 9), datetime(2023, 5, 16), datetime(2023, 5, 23), datetime(2023, 5, 30), ])
erik.add_availability([datetime(2023, 5, 2), datetime(2023, 5, 16), datetime(2023, 5, 23), ])
baptiste.add_availability([datetime(2023, 5, 2), datetime(2023, 5, 9), datetime(2023, 5, 30), ])
nicolas.add_availability([datetime(2023, 5, 2), datetime(2023, 5, 16), datetime(2023, 5, 23), datetime(2023, 5, 30), datetime(2023, 5, 13), ])
mathieu.add_availability([datetime(2023, 5, 30), ])
ulukai.add_availability([datetime(2023, 5, 23), datetime(2023, 5, 27)])

lea.add_availability([datetime(2023, 5, 2), datetime(2023, 5, 9), datetime(2023, 5, 16), datetime(2023, 5, 23), datetime(2023, 5, 30), datetime(2023, 5, 13), datetime(2023, 5, 27)])
veronique.add_availability([datetime(2023, 5, 2), datetime(2023, 5, 9), datetime(2023, 5, 23), datetime(2023, 5, 30), ])
natasha.add_availability([datetime(2023, 5, 2), datetime(2023, 5, 9), datetime(2023, 5, 16), datetime(2023, 5, 23), datetime(2023, 5, 30), ])
caroline.add_availability([datetime(2023, 5, 9), datetime(2023, 5, 16), datetime(2023, 5, 23), datetime(2023, 5, 30), ])

leads = [jean_yves, erik, baptiste, nicolas, mathieu, ulukai]
follows = [lea, veronique, natasha, caroline]
dates = [datetime(2023, 5, 2), datetime(2023, 5, 9), datetime(2023, 5, 16), datetime(2023, 5, 23), datetime(2023, 5, 30), datetime(2023, 5, 13), datetime(2023, 5, 27)]

def test_assignments():
    final_match = assign_dates(leads, follows, dates)

    print()

    for date, teachers in final_match.items():
        print(f"{date:%m-%d}: {teachers[0]} with {teachers[1]}")