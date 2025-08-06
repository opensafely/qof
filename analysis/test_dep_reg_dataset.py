from datetime import date

# 1) Import dataset from the dataset definition
from dep_reg_dataset import dataset

# Patient data for the FY23/24 with index date = "2024-04-01"
# Run the tests with the following command:
# opensafely exec ehrql:v1 assure analysis/test_dep_reg_dataset.py

# 2) Add test cases to test the dataset definition

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
    # Correctly not expected in population
    # Diagnosis after the index date
    2: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "practice_registrations": [
            {
                "start_date": date(2010, 1, 1),
            },
        ],
        "clinical_events": [
            {
                # First depression diagnosis (dep_codelist)
                "date": date(2024, 8, 1),
                "snomedct_code": "191601008",
            },
        ],
        "expected_in_population": False,
    },
    # Correctly not expected in population
    # Younger than 17yo at index date
    3: {
        "patients": {"date_of_birth": date(2010, 1, 1)},
        "practice_registrations": [
            {
                "start_date": date(2010, 1, 1),
            },
        ],
        "clinical_events": [
            {
                # First depression diagnosis (dep_codelist)
                "date": date(2022, 8, 1),
                "snomedct_code": "191601008",
            },
        ],
        "expected_in_population": False,
    },
    # Correctly not expected in population
    # Not registered at index date
    4: {
        "patients": {"date_of_birth": date(1960, 1, 1)},
        "practice_registrations": [
            {
                "start_date": date(1960, 1, 1),
                "end_date": date(2020, 1, 1),
            },
        ],
        "clinical_events": [
            {
                # First depression diagnosis (dep_codelist)
                "date": date(2022, 8, 1),
                "snomedct_code": "191601008",
            },
        ],
        "expected_in_population": False,
    },
    # Correctly not expected in population
    # Depression diagnosis resolved before index date
    5: {
        "patients": {"date_of_birth": date(1960, 1, 1)},
        "practice_registrations": [
            {
                "start_date": date(1960, 1, 1),
            },
        ],
        "clinical_events": [
            {
                # First depression diagnosis (dep_codelist)
                "date": date(2008, 6, 1),
                "snomedct_code": "191601008",
            },
            {
                # depression diagnosis resolved (depres_codelist)
                "date": date(2023, 1, 1),
                "snomedct_code": "196381000000100",
            },
        ],
        "expected_in_population": False,
    },
    # Correctly expected in population
    # depression diagnosis before index date
    6: {
        "patients": {"date_of_birth": date(1960, 1, 1)},
        "practice_registrations": [
            {
                "start_date": date(1960, 1, 1),
            },
        ],
        "clinical_events": [
            {
                # First depression diagnosis (dep_codelist)
                "date": date(2015, 6, 1),
                "snomedct_code": "191601008",
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "pat_age": 64,
            "depr_dat": date(2015, 6, 1),
            "depres_dat": None,
        },
    },
    # Correctly not expected in population
    # Code not from dep_codelist codelist
    7: {
        "patients": {"date_of_birth": date(1960, 1, 1)},
        "practice_registrations": [
            {
                "start_date": date(1960, 1, 1),
            },
        ],
        "clinical_events": [
            {
                # Code not in the codelist
                "date": date(2000, 6, 1),
                "snomedct_code": "1111111111",
            },
        ],
        "expected_in_population": False,
    },
    # Correctly not expected in population
    # Depression diagnosis recorded before min date (2006-01-01)
    8: {
        "patients": {"date_of_birth": date(1960, 1, 1)},
        "practice_registrations": [
            {
                "start_date": date(1960, 1, 1),
            },
        ],
        "clinical_events": [
            {
                # Diagnosis before min date
                "date": date(2000, 6, 1),
                "snomedct_code": "191601008",
            },
        ],
        "expected_in_population": False,
    },
}
