# 1) Import the required ehrql functions
from ehrql import create_dataset, codelist_from_csv

# 2) Import relevant tables from the TPP backend (OpenSAFELY-TPP)
from ehrql.tables.tpp import (
    clinical_events,
    patients,
    practice_registrations,
)

# 3) Load SNOMED-CT codelists from CSV files

# Depression codes
dep_codelist = codelist_from_csv(
    'codelists/nhsd-primary-care-domain-refsets-depr_cod.csv',
    column='code')
# Resolved depression codes
depres_codelist = codelist_from_csv(
    'codelists/nhsd-primary-care-domain-refsets-depres_cod.csv',
    column='code')

# 4) Define variables and the study population

# Utility function: return the most recent event (if any) for a patient matching a given codelist
def last_matching_event(events, codelist, where=True):
    return (
        events.where(where)
        .where(events.snomedct_code.is_in(codelist))
        .sort_by(events.date)
        .last_for_patient()
    )

# Quality Service Start Date (Index date)
qs_start_date = '2024-04-01' 

# Fixed date used in DEPR1_REG and DEPCC01 logic.
# Depression register: Patients aged at least 18 years old whose latest unresolved episode of depression is since 1st April 2006.
min_date = '2006-04-01'
# Create a dataset object
dataset = create_dataset()

# Identify patients who were registered on the index date
has_registration = practice_registrations.for_patient_on(
        qs_start_date
).exists_for_patient()

# Filter clinical events to only those on or before the index date
prior_events = clinical_events.where(clinical_events.date.is_on_or_before(qs_start_date))

# Field number: 4
# PAT_AGE: The age of the patient in full years at the index date.
dataset.pat_age = (patients
                   .age_on(qs_start_date))

# Field number 5: 
# DEPR_DAT: Date of the latest depression episode at the index date
dataset.depr_dat = last_matching_event(prior_events, dep_codelist).date

# Field number 6:
# DEPRES_DAT: Date of the most recent depression resolved code at the index date
dataset.depres_dat = last_matching_event(prior_events, depres_codelist).date

# DEP_REG rule 1: 
# Include patients that have their latest episode of unresolved depression on or after 1st April 2006.
dep1_reg_r1 = ((dataset.depr_dat.is_on_or_after(min_date))
               & (dataset.depres_dat.is_null()))

# DEP_REG rule 2:
# Include patients under the age of 18 on the index date
dep2_reg_r2 = dataset.pat_age < 18

# Define the final population:
# - Registered on index date
# - Meet rule 1 (active depression diagnosis)
# - Do not meet rule 2 (i.e. are 18 or older)
dataset.define_population(has_registration & dep1_reg_r1 & ~dep2_reg_r2)
