from ehrql import INTERVAL, case, create_measures, months, when, codelist_from_csv, create_dataset
from ehrql.tables.tpp import (
    clinical_events, 
    patients,
    practice_registrations,
)

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

index_date = "2024-03-31"
measures = create_measures()

### variables ###

selected_events = clinical_events.where(
    clinical_events.date.is_on_or_before(INTERVAL.end_date)
)

# date of the most recent hypertension diagnosis up to and including the achievement date
hyplat_dat = (
    selected_events.where(selected_events.snomedct_code.is_in(hyp_cod))
    .sort_by(selected_events.date)
    .last_for_patient()
    .date
)

# date of the most recent hypertension diagnosis resolved code recorded after the most recent hypertension diagnosis and up to and including the achievement date
hypres_dat = (
    selected_events.where(selected_events.snomedct_code.is_in(hypres_cod))
    .sort_by(selected_events.date)
    .last_for_patient()
    .date
)

# Rule for patients with a hypertension code that has not been resolved
hyp_reg_r1 = hyplat_dat.is_not_null() & hypres_dat.is_null() | (hyplat_dat > hypres_dat)

age = patients.age_on(INTERVAL.start_date)
age_band = case(
    when((age >= 0) & (age < 20)).then("0-19"),
    when((age >= 20) & (age < 40)).then("20-39"),
    when((age >= 40) & (age < 60)).then("40-59"),
    when((age >= 60) & (age < 80)).then("60-79"),
    when(age >= 80).then("80+"),
)

registration = practice_registrations.for_patient_on(INTERVAL.end_date)

# Measure defining the rate of patients with unresolved hypertension per age band and sex
measures.define_measure(
    name="diagnosis_by_age",
    numerator=hyp_reg_r1 == True,
    denominator=registration.exists_for_patient(),
    group_by={
        "age_band": age_band,
        "sex": patients.sex,
    },
    intervals=months(12).starting_on("2023-04-01"),
)

# Measure defining the rate of patients with resolved hypertension per age band and sex
measures.define_measure(
    name="resolved_by_age",
    numerator=hyp_reg_r1 == False,
    denominator=registration.exists_for_patient(),
    group_by={
        "age_band": age_band,
        "sex": patients.sex,
    },
    intervals=months(12).starting_on("2023-04-01"),
)