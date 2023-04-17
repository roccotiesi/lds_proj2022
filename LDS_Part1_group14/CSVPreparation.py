from CSVPreparationFunctions import *

## We import in lists the records of the main csv and the country code csv
answers_csv = openCSVFile ('answerdatacorrect.csv')
country_list = openCSVFile ('country-codes.csv')

# From the country code database we generate the dictionary of countries and
# continents, that will be used to generate the column 'Continent' in the
# main database. Also, it replace all country codes with the corrispondent
# country name.
country_dict, country_names = generateCountryDict (country_list)
answers_csv = generateContinentColumn (answers_csv, country_dict, country_names)

# This functions generate the column 'iscorrect'
answers_csv = generateIsCorrectColumn (answers_csv)

# Then, the list of dictionaries of every single date extracted from the
# main csv is created.
date_dict = generateDateDict (answers_csv)

# This function generates the column 'organization'
answer_csv = generateOrganizationColumn (answers_csv)

## With this function all the lists of dictionaries of all the tables
## are created from the main list (each of them requires futher 
## operations to be stored into csv files).
answers_dict, organization_dict, subject_dict, user_dict, geography_dict = generateTables (answer_csv)

# Given the list of dictionaries and the name of the key, this function
# generates new list with unique values based on that key.
organization_dict = dictUniqueValues (organization_dict, 'organizationid')
geography_dict = dictUniqueValues (geography_dict, 'Region')

# Generate the ids for the table geography.
geography_dict = generateIds (geography_dict, 'geoid')

# We assign the id to the correct dates in the tables answers and user, and
# then the correct id for each region in the table user.
answers_dict = assignDateKey (answers_dict, date_dict, 'DateAnswered', 'dateid')
user_dict = assignDateKey (user_dict, date_dict, 'DateOfBirth', 'dateofbirthid')
user_dict = assignRegionKey (user_dict, geography_dict, 'Region', 'geoid')

# The table user is completed so we can generate the new list of dictionaries
# with the unique ids.
user_dict = dictUniqueValues (user_dict, 'UserId')

## It imports all the records of the subject csv in a list.
## (we manually edit the header because of some odd characters
## in the column name 'Subject' that could create some problems).
subject_csv = openCSVFile ('subject_metadata.csv')
subject_csv[0][0] = 'SubjectId'

# From the data imported from the csv, it generates the list
# of dictionaries with all the subjects.
subject_table = generateSubjectDict (subject_csv)

# The list of subject ids extracted from the answers csv is modified
# leaving only unique values (unique lists of ids).
subject_dict = dictUniqueValues (subject_dict, 'SubjectId')

# In this way, we can assign unique ids to each sequence of subject ids.
subject_dict = generateIds (subject_dict, 'subjectid')

# From the dictionary with all the subject and the sequences of
# the ids of the subjects extracted from the main csv, we generate
# a list of descriptions. Each description contains the name of the
# subjects that are present in each sequence.
# This list is then added to the final list of dictionaries of the
# subjects and it is used to assign to each answer its subject id
# that represents the correct sequence.
subject_ids = generateSubjectList (subject_table, subject_dict)

# This function assigns to each record in answers the correct id
# of the sequence of subjects of that specific record.
answers_dict = assignDescriptionKey (answers_dict, subject_dict, 'SubjectId', 'subjectid')

# Each description is assigned to the dictionary from the list of
# sequences generated before.
subject_dict = addSubjectDescriptions (subject_dict, subject_ids)

## In the following three tables we remove some keys and their values
## because they are not present in the schema of the data warehouse.
## So they will be ready to be store in csv files and then imported
## on the SQL server.
answers_dict = dropKey (answers_dict, 'DateAnswered')
answers_dict = dropKey (answers_dict, 'SubjectId')
subject_dict = dropKey (subject_dict, 'SubjectId')
user_dict = dropKey (user_dict, 'RegionId')
user_dict = dropKey (user_dict, 'DateOfBirth')
user_dict = dropKey (user_dict, 'Region')

# Finally, all the list of dictionaries are extracted to their
# corresponding csv files.
saveToCSV (date_dict, 'date_final.csv')
saveToCSV (geography_dict, 'geo_final.csv')
saveToCSV (user_dict, 'user_final.csv')
saveToCSV (organization_dict, 'org_final.csv')
saveToCSV (subject_dict, 'subject_final.csv')
saveToCSV (answers_dict, 'answers_final.csv')