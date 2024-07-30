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

#Create index date and vector for which patients were registered then
index_date= "yyyy-mm-dd"
has_registration = practice_registrations.for_patient_on(index_date).exists_for_patient()


#Define the dataset (=cohort)




dataset.define_population(patients.date_of_birth.is_on_or_before("1999-12-31"))
dataset.define_population(has_registration)
