from datetime import date
from dep_reg_dataset import dataset

test_data = {
    # Test rule 1: Patient excluded due to case before April 2006
    1: {
        "practice_registrations": [{
            "start_date": date(2010, 1, 1),
        }], 
        "clinical_events": [{
            "snomedct_code": "104851000119103",
            "date": date(2005, 1, 1)
        }],
        "patients": {
            "date_of_birth": date(1950, 1, 1)
        },
        "expected_in_population": False,
    },
    # Test rule 2: Patients excluded due to depression resolved code
    # after depression incident case
    2: {
        "practice_registrations": [{
            "start_date": date(1950, 1, 1)
        }],
        "clinical_events": [
            {
            "snomedct_code": "104851000119103",
            "date": date(2009, 1, 1)},
            {
            "snomedct_code": "196381000000100",
            "date": date(2010, 1, 1)
        }],
        "patients": {
            "date_of_birth": date(1950, 1, 1)
        },
        "expected_in_population": False
    },
    # Test rule 3: Patients excluded due to being under 18
    3: {
        "practice_registrations": [{
            "start_date": date(1950, 1, 1)
        }],
        "clinical_events": [
            {
            "snomedct_code": "104851000119103",
            "date": date(2009, 1, 1)}],
        "patients": {
            "date_of_birth": date(2008, 1, 1)
        },
        "expected_in_population": False
    },
    # Patient who passess all rules
    4: {
        "practice_registrations": [{
            "start_date": date(1950, 1, 1)
        }],
        "clinical_events": [
            {
            "snomedct_code": "104851000119103",
            "date": date(2009, 1, 1)
            },
            {
            "snomedct_code": "196381000000100",
            "date": date(2008, 1, 1)
            }
        ], 
        "patients": {
            "date_of_birth": date(1990, 1, 1)
        },
        "expected_in_population": True,
        "expected_columns": {
            "pat_age": 34,
            "depr_dat": date(2009, 1, 1),
            "depres_dat": date(2008, 1, 1)
        }
    }
}