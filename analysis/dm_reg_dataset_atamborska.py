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
pat_age = (patients.age_on(index_date) >= 17)



#Create an object storing latest dates for Dx DM and Dx DM res for each patient

## Select the latest date with the diabetes code
latest_dm= XeventsX.where(XeventsX.dmd_code.is_in(dm_cod)).
sort_by(XeventX.date).
last_for_patient()

## Select the latest date with the diabetes resolved code
latest_dmres= XeventsX.where(XeventsX.dmd_code.is_in(dm_cod)).
sort_by(XeventX.date).
last_for_patient()


## Q: Do we need to attach these objects to the dataset?
#Q: Eg dataset.latest_dm= latest_dm
#Q: eg dataset.latest_dmres= latest_dmres
#Q: How will the dataset join these correctly>

#Define the dataset (=cohort) - using the rules

##Rule 1
###Latest diabetes diagnosis is not followed by a diabetes resolved code.
###Have a diabetes diagnosis in the patient record up to and including the achievement date.

dm_reg_r1= (dataset.latest_dmres < dataset.latest_dm) | (
    dataset.latest_dm.is_not_null() & dataset.latest_dmres.is_null()

##Rule 2
### Reject patients passed to this rule who are aged under 17 years old on the achievement date. Select the remaining patients.

    #dm_reg_r2= dataset.pat_age == T



# Create the population - Q: can you pass a rule to dataset.define_population or do you have to make a condition
dataset.define_population(dm_reg_r1)
vs. dataset.define_population(patients.date_of_birth < "1990-01-01")

