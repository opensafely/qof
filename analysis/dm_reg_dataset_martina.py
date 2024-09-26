from ehrql import (
    codelist_from_csv,
    create_dataset,  
    case, 
    when,
)

from ehrql.tables.tpp import (
    clinical_events,
    patients,
    practice_registrations,
)


index_date = "2024-03-31"

dataset = create_dataset()


dataset.configure_dummy_data(population_size=100)


# Code list

## DM
dm_code = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv",
    column="code",
)

## DM resolution
dm_res_cod = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dmres_cod.csv",
    column="code",
)

has_registration = practice_registrations.for_patient_on(index_date).exists_for_patient()

#Variables

#1. Age

## 1. a. Age variable
dataset.age = patients.age_on(index_date)

dataset.age_band = case(
        when(dataset.age < 20).then("0-19"),
        when(dataset.age < 40).then("20-39"),
        when(dataset.age < 60).then("40-59"),
        when(dataset.age < 80).then("60-79"),
        when(dataset.age >= 80).then("80+"),
        otherwise="missing",
)

## 1. b. Age rule
was_17_more_r2 = (patients.age_on(index_date) >= 17) & (
    patients.age_on(index_date) <= 110
)
##DM variables
###2.DM last diagnose
dataset.dmlat_dat = clinical_events.where(
        clinical_events.snomedct_code.is_in(dm_code)
).where(
        clinical_events.date.is_on_or_after(index_date)
).sort_by(
        clinical_events.date
).last_for_patient().date

###2.DM last resolved code
dataset.dmres_dat = clinical_events.where(
        clinical_events.snomedct_code.is_in(dm_res_cod)
).where(
        clinical_events.date.is_on_or_after(index_date)
).sort_by(
        clinical_events.date
).last_for_patient().date

dm_reg_r1 = (dataset.dmres_dat < dataset.dmlat_dat) | (
    dataset.dmlat_dat.is_not_null() & dataset.dmres_dat.is_null()
)



dataset.define_population(has_registration
                          & dm_reg_r1
                          & was_17_more_r2)