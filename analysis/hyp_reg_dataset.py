# 1) Import the required ehrql functions
from ehrql import create_dataset, codelist_from_csv

# 2) Import relevant tables from the TPP backend (OpenSAFELY-TPP)
from ehrql.tables.tpp import (
    clinical_events, 
    practice_registrations,
)

# 3) Load SNOMED-CT codelists from CSV files

# Hypertension codes
hyp_cod = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hyp_cod.csv",
    column="code"
)
# Hypertension resolved codes
hypres_cod = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-hypres_cod.csv",
    column="code"
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

# Field number: 6
# Date of the most recent hypertension diagnosis up to and including the achievement date
dataset.hyplat_dat = last_matching_event(prior_events, hyp_cod).date

# Fielt number: 7
# Date of the most recent hypertension diagnosis resolved code recorded after the most recent hypertension diagnosis and up to and including the achievement date
dataset.hypres_dat = last_matching_event(prior_events, hypres_cod).date


# HYP_REG rule:

# Include patients with a hypertension diagnosis on or before index date.
# Latest hypertension diagnosis is not followed by a hypertension resolved code.
dataset.hyp_reg_r1 = dataset.hyplat_dat.is_not_null() & dataset.hypres_dat.is_null() | (dataset.hyplat_dat > dataset.hypres_dat)

# Define the final population:
# - Registered on index date
# - Meet the rule (active diabetes diagnosis)
dataset.define_population(
    (has_registration) & dataset.hyp_reg_r1
    )
