# Task: Calulcate the monthly prevalence trends for the dementia QOF

# 1) Import the required functions from ehrql
from ehrql import codelist_from_csv
from ehrql import INTERVAL, case, create_measures, months, when

# 2) Import the tables of interest from TPP
from ehrql.tables.tpp import patients, practice_registrations, clinical_events

# 3) Import the codelists of interest
DEM_COD = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv",
    column = "code",
    )

# 4) Create series for numerator and denominator for each interval

## Numerator - number of people with diagnosis of dementia before the end of elegible period
selected_events = clinical_events.where(
    clinical_events.date.is_on_or_before(INTERVAL.end_date)
)

has_dementia = (
     selected_events.where(selected_events.snomedct_code.is_in(DEM_COD))
    .sort_by(selected_events.date)
    .last_for_patient()
    .date
)

## Denominator - number of people with practice registration before the beginning of the interval 
## and with no deregsotration or with reregistration after the end of each interval
was_registered = (
    practice_registrations.where(
    practice_registrations.start_date.is_on_or_before(INTERVAL.start_date) &
    (practice_registrations.end_date.is_null() | 
     practice_registrations.end_date.is_on_or_after(INTERVAL.end_date))
     )
    .sort_by(practice_registrations.start_date)
    .first_for_patient()
    .start_date
)

# Possibly another way of expressing: practice_registrations.for_patient_on(index_date).exists_for_patient() 

# Create measures framework
measures = create_measures()

measures.define_measure(
    name="dem_qof_monthly",
    numerator= has_dementia.is_not_null(),
    denominator= was_registered.is_not_null(),
    intervals=months(12).starting_on("2023-04-01"),
)

# The output is a dataframe of measure name, interval_start, 
# interval_end, ratio, numerator, denominator.