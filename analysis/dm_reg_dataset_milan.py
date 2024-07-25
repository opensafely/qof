from pathlib import Path

from ehrql import create_dataset
from ehrql.codes import codelist_from_csv

from ehrql.tables.tpp import (
    patients,
    practice_registrations,
)

CODELIST_DIR = Path("codelists")

# Cluster name: DM_COD
# Description: Diabetes mellitus codes
# Refset ID: ^999004691000230108
dm_cod = codelist_from_csv(
    CODELIST_DIR / "nhsd-primary-care-domain-refsets-dm_cod.csv",
    column="code",
)

# Cluster name: DMRES_COD
# Description: Diabetes resolved codes
# Refset ID: ^999003371000230102
dm_res_cod = codelist_from_csv(
    CODELIST_DIR / "nhsd-primary-care-domain-refsets-dmres_cod.csv",
    column="code",
)

index_date = "2024-03-31"
dataset = create_dataset()

has_registration = practice_registrations.for_patient_on(index_date).exists_for_patient()
dataset.define_population(has_registration)

# Field number: 2
# REG_DAT: The most recent date that the patient registered for GMS, where
# this registration occurred on or before the achievement date.
dataset.reg_dat = practice_registrations.for_patient_on(index_date).start_date

# Field number: 4
# PAT_AGE: The age of the patient in full years at the achievement date.
dataset.pat_age = patients.age_on(index_date)
