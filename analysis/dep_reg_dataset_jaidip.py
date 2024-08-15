from ehrql import create_dataset
from ehrql.codes import codelist_from_csv

from ehrql.tables.tpp import (
    clinical_events,
    patients,
    practice_registrations,
)

dataset = create_dataset()
qs_start_date = '2024-04-01' # Quality Service Start Date
min_date = '2006-04-01' # Have their latest first or new episode of depression on or after 1 st April 2006.

# import codelists
dep_codelist = codelist_from_csv(
    'codelists/nhsd-primary-care-domain-refsets-depr_cod.csv',
    column='code')
depres_codelist = codelist_from_csv(
    'codelists/nhsd-primary-care-domain-refsets-depres_cod.csv',
    column='code')

# inclusion criteria
has_registration = (practice_registrations
                    .for_patient_on(qs_start_date)
                    .exists_for_patient())

'''
Create disease variables
- DEPR_DAT = Latest date of depression diagnosis
- DEPRES_DAT = Latest depression resolved date
- PAT_AGE = Age at quality service start date
'''
dataset.DEPR_DAT = ((clinical_events.
                    where(clinical_events
                          .snomedct_code
                          .is_in(dep_codelist))
                          ).sort_by(clinical_events.date)
                          .last_for_patient()
                          .date)
dataset.DEPRES_DAT = (clinical_events
                      .where(clinical_events
                             .snomedct_code
                             .is_in(depres_codelist))
                             .sort_by(clinical_events.date)
                             .last_for_patient()
                             .date)
dataset.PAT_AGE = (patients
                   .age_on(qs_start_date))

'''
Creating rules
1. If DEPR_DAT >= 01/04/2006
    AND
    If DEPRES_DAT = Null
2. If PAT_AGE >= 18 years
'''
dep1_reg_r1 = ((dataset.DEPR_DAT.is_on_or_after(min_date))
               & (dataset.DEPRES_DAT.is_null()))
dep2_reg_r2 = dataset.PAT_AGE >= 18

dataset.define_population(has_registration & dep1_reg_r1 & dep2_reg_r2)
