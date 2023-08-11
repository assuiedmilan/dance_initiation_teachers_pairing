from datetime import datetime

from data.dancer import Dancer
from enumerations.dancer_level import DancerLevel
from resolver.assign_dates import assign_dates

jean_yves = Dancer("JY", DancerLevel.EXPERT, is_lead=True)
erik = Dancer("Erik", DancerLevel.BEGINNER, is_lead=True)
baptiste = Dancer("Baptiste", DancerLevel.MEDIUM, is_lead=True)
nicolas = Dancer("Nicolas", DancerLevel.MEDIUM, is_lead=True)
mathieu = Dancer("Mathieu", DancerLevel.MEDIUM, is_lead=True)
ulukai = Dancer("Ulukai", DancerLevel.BEGINNER, is_lead=True)

lea = Dancer("Lea", DancerLevel.EXPERT, is_lead=False)
veronique = Dancer("Veronique", DancerLevel.EXPERT, is_lead=False)
natasha = Dancer("Natasha", DancerLevel.BEGINNER, is_lead=False)
caroline = Dancer("Caroline", DancerLevel.BEGINNER, is_lead=False)

jean_yves.add_availability([datetime(2023, 6, 13), datetime(2023, 6, 20), datetime(2023, 6, 27)])
erik.add_availability([datetime(2023, 6, 13), datetime(2023, 6, 20), datetime(2023, 6, 27)])
baptiste.add_availability([datetime(2023, 6, 10), datetime(2023, 6, 13), ])
nicolas.add_availability([])
mathieu.add_availability([])
ulukai.add_availability([datetime(2023, 6, 10), datetime(2023, 6, 20), datetime(2023, 6, 27)])

lea.add_availability([datetime(2023, 6, 10), datetime(2023, 6, 13), ])
veronique.add_availability([datetime(2023, 6, 13), ])
natasha.add_availability([datetime(2023, 6, 13), datetime(2023, 6, 20), datetime(2023, 6, 27)])
caroline.add_availability([datetime(2023, 6, 13), datetime(2023, 6, 20), ])

leads = [jean_yves, erik, baptiste, nicolas, mathieu, ulukai]
follows = [lea, veronique, natasha, caroline]
dates = [datetime(2023, 6, 10), datetime(2023, 6, 13), datetime(2023, 6, 20), datetime(2023, 6, 27)]

def test_assignments():
    final_match = assign_dates(leads, follows, dates)

    print()

    for date, teachers in final_match.items():
        print(f"{date:%m-%d}: {teachers[0]} with {teachers[1]}")