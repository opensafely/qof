# Measures framework cannot be tested in this way - retire the script
# Run this using the command: opensafely exec ehrql:v1 assure analysis test_dem_qof_measures_arina.py

from datetime import date
from dem_qof_measures_arina.py import dataset

test_data = {
    # Patient expected in the population
    1: {
        # Rule 1: Is registered  
        "practice_registrations": [
            {
                "start_date": date(2009, 6, 7),
                "end_date": NULL,
            },
        ],
        # Rule 2: Has dementia
        "clinical_events": [
            {
                "date": date(2015, 7, 8)
                "snomedct_code": "429998004"
            }
        ]
        "expected_in_population": True,
    }
    # Patient not expected the population: no dementia
    2: {
        # Rule 1: Is registered  
        "practice_registrations": [
            {
                "start_date": date(2009, 6, 7),
                "end_date": NULL,
            },
        ],
        # Rule 2: No clinical events
        "clinical_events": [{}],
        "expected_in_population": False,
    }
    # Patient not expected in population, not registered
    3:{
        # Rule 1: Not registered during the interval
        "practice_registrations": [
            {
                "start_date": date(2009, 6, 7),
                "end_date": date(2014, 1, 1),
            },
        ],
        # Rule 2: Has dementia
        "clinical_events": [
            {
                "date": date(2015, 7, 8)
                "snomedct_code": "429998004"
            }
        ]
        "expected_in_population": False,
    }
}