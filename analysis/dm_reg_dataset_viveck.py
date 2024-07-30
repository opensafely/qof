from ehrql import codelist_from_csv
from ehrql import create_dataset
from ehrql.tables.tpp import (
    clinical_events, 
    patients,
    practice_registrations,
)

# Diabetes mellitus codes
dm_cod = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv",
    column="code"
)
# Diabetes resolved codes
dmres_cod = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dmres_cod.csv",
    column="code"
)

index_date = "2024-03-31"

dataset = create_dataset()
has_registration = practice_registrations.for_patient_on(index_date).exists_for_patient()
dataset.define_population(has_registration)

# variables

# date of the most recent diabetes diagnosis up to and including the achievement date
dataset.dmlat_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(dm_cod))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

# date of the most recent diabetes diagnosis resolved code recorded after the most recent diabetes diagnosis and up to and including the achievement date
dataset.dmres_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(dmres_cod))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

# age of the patient in full years at the achievement date
dataset.pat_age = patients.age_on(index_date)

# rules

# Pass to the next rule all patients from the specified population who meet both of the criteria below:
# Have a diabetes diagnosis in the patient record up to and including the achievement date.
# Latest diabetes diagnosis is not followed by a diabetes resolved code.
dataset.dm_reg_r1 = dataset.dmres_dat.is_null() & dataset.dmlat_dat.is_not_null() | (dataset.dmlat_dat > dataset.dmres_dat)

#Reject patients passed to this rule who are aged under 17 years old on the achievement date.
dataset.dm_reg_r2 = dataset.pat_age < 17

