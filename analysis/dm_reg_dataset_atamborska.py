#Import function create_dataset
from ehrql import create_dataset

#Import the tables of the variables you need
from ehrql.tables.tpp import patients, practice_registrations, clinical_events

## could use from ehrql.tables.core or from ehrql.tables.emis

#Create an empty dataset
dataset = create_dataset()

#Create objects containing codelists - these will be used to define the dataset
codelist_path= Path("codelists")
dm_cod= codelist_from_csv(codelist_path/ "nhsd-primary-care-domain-refsets-dm_cod.csv",
    column="code",
)
dmres_cod= codelist_from_csv(codelist_path/"nhsd-primary-care-domain-refsets-dm_codres.csv")

#Create index date 
index_date= "2024-03-31"

#Create a boolean vector for which patients were registered up until the index date
registered = practice_registrations.for_patient_on(index_date).exists_for_patient()

#Create a boolean vector to filter patients >17 at index date
PAT_AGE = (patients.age_on(index_date) >= 17)

#Create a boolean vector to select patients with appropriate an DM code

DMLAT_DAT
DMRES_DAT




#Define the dataset (=cohort) - using the rules

##Rule 1
###Latest diabetes diagnosis is not followed by a diabetes resolved code.
###Have a diabetes diagnosis in the patient record up to and including the achievement date.

dm_reg_r1= (dataset.dmres_dat < dataset.dmlat_dat) | (
    dataset.dmlat_dat.is_not_null() & dataset.dmres_dat.is_null()

##Rule 2
### Reject patients passed to this rule who are aged under 17 years old on the achievement date. Select the remaining patients.
#dm_reg_r2= dataset.age = T



# Create the population
dataset.define_population(dm_reg_r1)


