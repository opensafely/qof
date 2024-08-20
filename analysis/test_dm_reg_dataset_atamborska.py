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
    }
}
