from ehrql import INTERVAL, case, create_measures, months, when, codelist_from_csv, create_dataset
from ehrql.tables.tpp import (
    clinical_events, 
    patients,
    practice_registrations,
    addresses
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
dataset = create_dataset()

measures = create_measures()

### variables ###

# date of the most recent hypertension diagnosis up to and including the achievement date
hyplat_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(hyp_cod) & clinical_events.date.is_on_or_before(INTERVAL.end_date))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

# date of the most recent hypertension diagnosis resolved code recorded after the most recent hypertension diagnosis and up to and including the achievement date
hypres_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(hypres_cod) & clinical_events.date.is_on_or_before(INTERVAL.end_date))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

age = patients.age_on(INTERVAL.start_date)
age_band = case(
    when((age >= 0) & (age < 20)).then("0-19"),
    when((age >= 20) & (age < 40)).then("20-39"),
    when((age >= 40) & (age < 60)).then("40-59"),
    when((age >= 60) & (age < 80)).then("60-79"),
    when(age >= 80).then("80+"),
)

imd = addresses.for_patient_on(INTERVAL.end_date).imd_rounded
imd_quintile = case(
    when((imd >=0) & (imd < int(32844 * 1 / 5))).then("1 (most deprived)"),
    when(imd < int(32844 * 2 / 5)).then("2"),
    when(imd < int(32844 * 3 / 5)).then("3"),
    when(imd < int(32844 * 4 / 5)).then("4"),
    when(imd < int(32844 * 5 / 5)).then("5 (least deprived)"),
    otherwise="unknown"
)


# proportion of patients per month who were successfully treated for hypertension grouped by age band and index of multiple deprivation
# Could be a useful measure to look at which age groups / imd are likely to get a resolved diagnosis (access to care) 
measures.define_measure(
    name="resolved_diagnosis_by_age",
    numerator=hypres_dat.is_not_null(),
    denominator=patients.exists_for_patient(),
    group_by={
        "age_band": age_band,
        "imd": imd_quintile,
    },
    intervals=months(6).starting_on("2023-04-01"),
)

# proportion of patients per month who were diagnosed for hypertension grouped by age band and index of multiple deprivation
# Could be a useful measure to look at which age groups / imd are likely to get diagnosed(access to care and potentially contributing risk factors to positive diagnosis) 
measures.define_measure(
    name="diagnosis_by_age",
    numerator=hyplat_dat.is_not_null(),
    denominator=patients.exists_for_patient(),
    group_by={
        "age_band": age_band,
        "imd": imd_quintile,
    },
    intervals=months(6).starting_on("2023-04-01"),
)