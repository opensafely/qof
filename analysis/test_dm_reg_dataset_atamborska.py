# Set up
from datetime import date
from dm_reg_dataset_atamborska import dataset

test_data = {
    # Patient accepted in the dataset
    1: {
        "patients": {"date_of_birth": date(1992, 1, 1)},
        "practice_registrations": [
            {
                # First registration
                "start_date": date(1994, 1, 1),
                "end_date": date(1999, 1, 1),
            },
            {
                # Second registration
                "start_date": date(1999, 1, 2),
            },
        ],
        "clinical_events": [
            # First clinical event
            {
                "snomedct_code": "313435000",
                "date": date(2000, 4, 13),
            },
            # Second clinical event
            {
                "snomedct_code": "420270002",
                "date": date(2004, 1, 17),
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "pat_age": 32,
            "registered": True,
            "latest_dm": date(2004, 1, 17),
            "latest_dmres": None,
        },
    },
    # Patient not accepted in the dataset: no active registration
    2: {
        "patients": {"date_of_birth": date(1992, 1, 1)},
        "practice_registrations": [
            {
                # First registration
                "start_date": date(1994, 1, 1),
                "end_date": date(1999, 1, 1),
            },
            {
                # Second registration
                "start_date": date(1999, 1, 2),
                "end_date": date(2005, 1, 1),
            },
        ],
        "clinical_events": [
            # First clinical event
            {
                "snomedct_code": "313435000",
                "date": date(2000, 4, 13),
            },
            # Second clinical event
            {
                "snomedct_code": "420270002",
                "date": date(2004, 1, 17),
            },
        ],
        "expected_in_population": False,
    },
    # Patient not accepted in the dataset: diabetes resolved
    3: {
        "patients": {"date_of_birth": date(1992, 1, 1)},
        "practice_registrations": [
            {
                # First registration
                "start_date": date(1994, 1, 1),
                "end_date": date(1999, 1, 1),
            },
            {
                # Second registration
                "start_date": date(1999, 1, 2),
            },
        ],
        "clinical_events": [
            # First clinical event
            {
                "snomedct_code": "313435000",
                "date": date(2000, 4, 13),
            },
            # Second clinical event
            {
                "snomedct_code": "315051004",
                "date": date(2004, 1, 17),
            },
        ],
        "expected_in_population": False,
    },
    # Patient accepted in the dataset: diabetes resolved in the past, then another episode
    4: {
        "patients": {"date_of_birth": date(1992, 1, 1)},
        "practice_registrations": [
            {
                # First registration
                "start_date": date(1994, 1, 1),
                "end_date": date(1999, 1, 1),
            },
            {
                # Second registration
                "start_date": date(1999, 1, 2),
            },
        ],
        "clinical_events": [
            # First clinical event
            {
                "snomedct_code": "313435000",
                "date": date(2000, 4, 13),
            },
            # Second clinical event
            {
                "snomedct_code": "315051004",
                "date": date(2004, 1, 17),
            },
            # Third clinical event
            {"snomedct_code": "313436004", "date": date(2015, 1, 1)},
        ],
        "expected_in_population": True,
        "expected_columns": {
            "pat_age": 32,
            "registered": True,
            "latest_dm": date(2015, 1, 1),
            "latest_dmres": date(2004, 1, 17),
        },
    },
    # Patient not accepted in the dataset: too young
    5: {
        "patients": {"date_of_birth": date(2008, 1, 1)},
        "practice_registrations": [
            {
                # First registration
                "start_date": date(2017, 1, 1),
                "end_date": date(2022, 1, 1),
            },
            {
                # Second registration
                "start_date": date(2022, 1, 2),
            },
        ],
        "clinical_events": [
            # First clinical event
            {
                "snomedct_code": "420270002",
                "date": date(2018, 1, 1),
            },
        ],
        "expected_in_population": False,
    },
}
