from ehrql import INTERVAL, create_measures, months, codelist_from_csv, case, when
from ehrql.tables.tpp import *

# instantiate measures
measures = create_measures()

# Import codelists
dep_codelist = codelist_from_csv('codelists/nhsd-primary-care-domain-refsets-depr_cod.csv',
                                 column = 'code')
depres_codelist = codelist_from_csv('codelists/nhsd-primary-care-domain-refsets-depres_cod.csv',
                                    column = 'code')

# important dates
qs_start_date = '2023-04-01' # Quality Service Start Date
min_date = '2006-04-01' # Have their latest first or new episode of depression on or after 1 st April 2006

# inclusion criteria
has_registration = (practice_registrations
                    .spanning(INTERVAL.start_date, INTERVAL.end_date)
                    .exists_for_patient())

'''
Create disease variables
- DEPR_DAT = Latest date of depression diagnosis
- DEPRES_DAT = Latest depression resolved date
- PAT_AGE = Age at quality service start date
'''
DEPR_DAT = ((clinical_events.
                    where(clinical_events
                          .snomedct_code
                          .is_in(dep_codelist))
                          ).sort_by(clinical_events.date)
                          .last_for_patient()
                          .date)
DEPRES_DAT = (clinical_events
                      .where(clinical_events
                             .snomedct_code
                             .is_in(depres_codelist))
                             .sort_by(clinical_events.date)
                             .last_for_patient()
                             .date)
PAT_AGE = (patients.age_on(INTERVAL.start_date))

'''
Creating rules
1. If DEPR_DAT >= 01/04/2006
    AND
    If DEPRES_DAT = Null
2. If PAT_AGE >= 18 years
'''
dep1_reg_r1 = ((DEPR_DAT.is_on_or_after(min_date))
               & (DEPRES_DAT.is_null()))
dep1_reg_r2 = PAT_AGE >= 18

# Define measures
dep_in_interval = DEPR_DAT.is_during(INTERVAL)

# Stratification groups
sex = patients.sex
age_band = case(
    when((PAT_AGE >= 18) & (PAT_AGE <= 21)).then("Young adult"),
    when((PAT_AGE >= 22) & (PAT_AGE <= 64)).then("Adult"),
    when(PAT_AGE >= 65).then("Elderly")
)

# Create measures
measures.define_measure(
    name = 'Monthly_Prevalence',
    numerator = dep_in_interval,
    denominator = has_registration & dep1_reg_r1 & dep1_reg_r2,
    intervals = months(12).starting_on(qs_start_date),
    group_by = {
        'Sex': sex,
        'Age': age_band
    }
)