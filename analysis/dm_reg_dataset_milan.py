# Objective: Create a dataset with columns of interest, taken from TPP tables

from pathlib import Path

# 1) Import the required ehrql functions
from ehrql import create_dataset, codelist_from_csv

# 2) Import relevant tables from the TPP backend (OpenSAFELY-TPP)
from ehrql.tables.tpp import (
    clinical_events,
    patients,
    practice_registrations,
)

CODELIST_DIR = Path("codelists")

# 3) Load SNOMED-CT codelists from CSV files

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

# 4) Define variables and the study population

# Utility function: return the most recent event (if any) for a patient matching a given codelist
def last_matching_event(events, codelist, where=True):
    return (
        events.where(where)
        .where(events.snomedct_code.is_in(codelist))
        .sort_by(events.date)
        .last_for_patient()
    )

# Define the index date for this dataset (e.g. reporting period end)
index_date = "2024-03-31"
# Create a dataset object
dataset = create_dataset()

# Identify patients who were registered on the index date
has_registration = practice_registrations.for_patient_on(
    index_date
).exists_for_patient()

# Filter clinical events to only those on or before the index date
prior_events = clinical_events.where(clinical_events.date.is_on_or_before(index_date))

# Field number: 4
# PAT_AGE: The age of the patient in full years at the index date.
dataset.pat_age = patients.age_on(index_date)

# Field number: 6
# DMLAT_DAT: Date of the most recent diabetes diagnosis on or before index date
dataset.dmlat_dat = last_matching_event(prior_events, dm_cod).date

# Field number: 7
# DMRES_DAT: Date of the most recent diabetes diagnosis resolved code
# recorded after the most recent diabetes diagnosis (if any)
dataset.dmres_dat = last_matching_event(prior_events, dm_res_cod).date

# DM_REG rule 1:
# Include patients with a diabetes diagnosis and no subsequent resolution
# (i.e. latest resolved code is earlier than diagnosis, or no resolved code recorded)
dataset.dm_reg_r1 = (dataset.dmres_dat < dataset.dmlat_dat) | (
    dataset.dmlat_dat.is_not_null() & dataset.dmres_dat.is_null()
)

# DM_REG rule 2:
# Include patients under 17 years of age on the index date
dataset.dm_reg_r2 = dataset.pat_age < 17

# Define the final population:
# - Registered on index date
# - Meet rule 1 (active diabetes diagnosis)
# - Do not meet rule 2 (i.e. are 17 or older)
dataset.define_population(has_registration & dataset.dm_reg_r1 & ~dataset.dm_reg_r2)