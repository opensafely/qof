from datetime import date
from hyp_reg_dataset import dataset

test_data = {

    # Correctly not expected in population
    # No clinical events
    1: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "practice_registrations": [
            {
                "start_date": date(2010, 1, 1),
            },
        ],
        "clinical_events": [{}],
        "expected_in_population": False,
    },

    # Correctly expected in population
    # Most recent hypertension diagnosis before index date
    2: {
        "patients": {"date_of_birth": date(1950,1,1)},
        "practice_registrations": [
            {
                "start_date": date(2010,1,1)
            }
        ],
        "clinical_events": [
            {
                # First hypertension diagnosis
                "date": date(2000,1,1),
                "snomedct_code": "38341003",
            },
            {
                # Second hypertension diagnosis
                "date": date(2020,3,3),
                "snomedct_code": "38341003",
            }
        ],
        "expected_in_population": True,
        "expected_columns": {
            "hyplat_dat": date(2020,3,3),
            "hypres_dat": None,
            "hyp_reg_r1": True, 
        },

    },

    # Correctly expected in population
    # Most recent resolved hypertension diagnosis before index date
    3: {
        "patients": {"date_of_birth": date(1950,1,1)},
        "practice_registrations": [
            {
                "start_date": date(2010,1,1)
            }
        ],
        "clinical_events": [
            {
                # First hypertension diagnosis
                "date": date(2000,1,1),
                "snomedct_code": "38341003",
            },
            {
                # Second hypertension diagnosis
                "date": date(2020,3,3),
                "snomedct_code": "38341003",
            },
            {
                # Third hypertension diagnosis
                "date": date(2024,2,2),
                "snomedct_code": "38341003"
            },
            {
                # First resolved diagnosis
                "date": date(2000,2,1),
                "snomedct_code": "162659009"
            },
            {
                # Second resolved diagnosis
                "date": date(2020,3,4),
                "snomedct_code": "162659009"
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "hyplat_dat": date(2024,2,2),
            "hypres_dat": date(2020,3,4),
            "hyp_reg_r1": True, 
        },

    },
    # Correctly not expected in population
    # Resolved diagnosis before index date
    4: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "practice_registrations": [
            {
                "start_date": date(2010, 1, 1),
            },
        ],
        "clinical_events": [
            {
               # First hypertension diagnosis
                "date": date(2000,1,1),
                "snomedct_code": "38341003", 
            },
            {
               # First resolved diagnosis
                "date": date(2000,2,1),
                "snomedct_code": "162659009" 
            },
            ],
        "expected_in_population": False,
    },

    # Correctly not expected in population
    # Patient not registered at practice
    5: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "practice_registrations": [
            {
                "start_date": date(2010, 1, 1),
                "end_date": date(2020,1,2),
            },
        ],
        "clinical_events": [
            {
               # First hypertension diagnosis
                "date": date(2000,1,1),
                "snomedct_code": "38341003", 
            },
            ],
        "expected_in_population": False,
    },

    # Correctly not expected in population
    # Patient diagnosed after index date
    6: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "practice_registrations": [
            {
                "start_date": date(2010, 1, 1),
            },
        ],
        "clinical_events": [
            {
               # First hypertension diagnosis
                "date": date(2024,4,1),
                "snomedct_code": "38341003", 
            },
            ],
        "expected_in_population": False,
    },

    # Correctly not expected in population
    # Patient diagnosed with a cold before index date
    7: {
        "patients": {"date_of_birth": date(1960, 1, 1)},
        "practice_registrations": [
            {
                "start_date": date(1960, 1, 1),
            },
        ],
        "clinical_events": [
            {
                # First cold diagnosis
                "date": date(2000, 6, 1),
                "snomedct_code": "82272006",
            },
            ],
        "expected_in_population": False,
    },
 }