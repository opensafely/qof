from ehrql import INTERVAL, create_measures, months, case, when
from ehrql.tables.tpp import (
    practice_registrations,
    patients,
    clinical_events,
    addresses,
)
from dm_reg_dataset import dm_cod

measures = create_measures()
measures.configure_dummy_data(population_size=100)
measures.configure_disclosure_control(enabled=False)

start_date = "2017-03-31"

# Is patient registered to a GP practice? (Boolean variable)
has_registration = practice_registrations.for_patient_on(
    INTERVAL.end_date
).exists_for_patient()

# Select clinical events for measures interval
selected_events = clinical_events.where(
    clinical_events.date.is_on_or_between(
        INTERVAL.start_date,
        INTERVAL.end_date,
    )
)

# Select clinical events with a diabetes diagnosis code (occurence - how many patients had a diabetes-coded clinical event during the interval)
dm_occurence = selected_events.where(
    selected_events.snomedct_code.is_in(dm_cod)
).exists_for_patient()

# Age band groupings
age = patients.age_on(INTERVAL.start_date)
age_band = case(
    when((age >= 0) & (age < 20)).then("0-19"),
    when((age >= 20) & (age < 40)).then("20-39"),
    when((age >= 40) & (age < 60)).then("40-59"),
    when((age >= 60) & (age < 80)).then("60-79"),
    when(age >= 80).then("80+"),
    when(age.is_null()).then("Missing"),
)

# IMD groupings
imd = addresses.for_patient_on(INTERVAL.start_date).imd_rounded
max_imd = 32844
imd_quintile = case(
    when((imd >= 0) & (imd < int(max_imd * 1 / 5))).then("1 (Most Deprived)"),
    when(imd < int(max_imd * 2 / 5)).then("2"),
    when(imd < int(max_imd * 3 / 5)).then("3"),
    when(imd < int(max_imd * 4 / 5)).then("4"),
    when(imd <= max_imd).then("5 (Least Deprived)"),
    otherwise="Missing",
)

# Defining default denominators (as we are using the same denominator and interval for each measure here)
measures.define_defaults(
    denominator=(has_registration & (patients.age_on(INTERVAL.start_date) > 17)),
    intervals=months(12).starting_on(start_date),
)

# This measure looks at the number of patients with a diabetes diagnosis code per interval
measures.define_measure(name="dm_occurence", numerator=dm_occurence)

# This measure looks at the number of patients with a diabetes diagnosis code per interval by age band
measures.define_measure(
    name="dm_occurence_by_age", numerator=dm_occurence, group_by={"age_band": age_band}
)

# This measure looks at the number of patients with a diabetes diagnosis code per interval by IMD
measures.define_measure(
    name="dm_occurence_by_imd", numerator=dm_occurence, group_by={"imd": imd_quintile}
)
