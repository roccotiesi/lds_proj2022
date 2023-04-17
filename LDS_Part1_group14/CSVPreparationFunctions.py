###     CSV TO SQL  ###
###     GROUP_14    ###

### IMPORTING LIBRARIES
import csv

### FUNCTIONS ###
##
## With this function we extract all the content of the csv in a list.
## The result is a list of lists and each list contains all the element of
## a single row of the csv.
## It returns the list.
def openCSVFile (file_dir):
    items = []

    with open(file_dir, "r") as csvfile:
        reader_a = csv.reader(csvfile, delimiter=",")
        for row in reader_a:
            items.append(row)
    
    print(f'-> Loading of {file_dir} completed')
    return items


## This function renames all the continent from a shorter version to
## a longer one to be more understandable in the database.
## It returns the new list of continents.
def renameContinent (continent):
    continent = [e.replace('AS', 'Asia') for e in continent]
    continent = [e.replace('EU', 'Europe') for e in continent]
    continent = [e.replace('AF', 'Africa') for e in continent]
    continent = [e.replace('OC', 'Oceania') for e in continent]
    continent = [e.replace('NA', 'Nord America') for e in continent]
    continent = [e.replace('SA', 'Sud America') for e in continent]
    continent = [e.replace('AN', 'Antarctica') for e in continent]

    print('-> All continents renamed')
    return continent

## This function, given the list extracted from the csv file of country codes,
## generates a dictionary with country code as key and the corresponding
## continent as value.
## It returns the dictionary
def generateCountryDict (country_list):
    ## It creates two separate lists to extract all the country codes
    ## and all the continents
    country_code, continent, name = [], [], []

    for i in range (1, len(country_list)):
        country_code.append(country_list[i][0])
        continent.append(country_list[i][2])
        name.append(country_list[i][3])

    ## It calls the function to rename all the continents
    continent = renameContinent(continent)

    ## It creates the final dictionary to store all the keys and values
    ## In the end, it returns the dictionary
    country_dict = {}

    for item1, item2 in zip(country_code, continent):
        country_dict.update({item1: item2})
    
    ## It creates the dictionary with the country code as keys and the
    ## country name as values, to later replace the names in the
    ## table
    country_names = {}

    for item1, item2 in zip(country_code, name):
        country_names.update({item1: item2})

    print('-> Country dictionary generated')
    return country_dict, country_names

## This function create the new column 'Continent' in the original list
## with all the data. First, a new column name is added at the end of the
## "first row", in the header. Then, for each row of the list, it checks
## the country code (in the 17th position) and adds at the end of the
## list the correct continent name, extracted from the dictionary.
## It also replace every country code with it corrispondent country name
## extracted from the csv of countries.
## It returns the new list.
def generateContinentColumn (items, country_dict, country_names):
    items[0].append('Continent')

    for i in range(1, len(items)):
        curr_country = (items[i][16])
        curr_continent = country_dict[curr_country]
        items[i].append(curr_continent)
        items[i][16] = country_names[items[i][16]]
    
    print('-> New column Continent added')
    return items

## With this function a new column 'iscorrect' is added to the list.
## Each element of this column contains the value 1 if the correct answer
## and the given answer by the user is the same (4th and 5th position
## in the original csv), 0 otherwise.
## It returns the new list.
def generateIsCorrectColumn (items):
    items[0].append('iscorrect')

    for i in range(1, len(items)):
        if items[i][3] == items[i][4]:
            items[i].append(1)
        else:
            items[i].append(0)
    
    print ('-> New column iscorrect added')
    return items

## This function, given the month, returns the
## correct quarter in the format QX.
def getQuarter (date_month, date_year):
    if int(date_month) > 0 and int(date_month) <= 12:
        return str(f'Q{(int(date_month) - 1) // 3 + 1}_{date_year}')
    else:
        return str('WRONG FORMAT')

## This function extract all the dates from the original csv (from the list)
## and generates the list of dictionaries of all the elements that
## will form the final table "date"
## It returns the list of dictionaries.
def generateDateDict (items):
    
    ## We use a set to store all the dates without duplicates.
    date_set = set()

    for i in range (1, len(items)):
        date_set.add(items[i][6]) #date of birth
        date_set.add(items[i][8][0:10]) #date of answer, without hour
    
    ## Using a counter, we create all the ids for the dates, starting
    ## from the value 1.
    date_id = []
    c = 1

    for i in date_set:
        date_id.append(c)
        c+=1
    
    ## It transforms the set into a list to be accessible later on and
    ## it creates all the lists for each field of the final
    ## dictionary/table
    date_list = list(date_set)
    date_day, date_month, date_year, date_quarter = [], [], [], []
    
    ## With this for loop, year, month, day and quarter (generated with the
    ## previous function) are extracted from the dates in the set and
    ## they are inserted into the respective lists.
    for i in date_list:
        date_year.append(i[0:4])
        date_month.append(i[0:4] + i[5:7])
        date_day.append(i[0:4] + i[5:7] + i[8:10])
        date_quarter.append(getQuarter(i[5:7], i[0:4]))
    
    ## We need to create the list of attributes of the final table that
    ## are used as keys of the dictionary.
    date_header = ['dateid', 'date', 'day', 'month', 'year', 'quarter']

    ## First, the empty list is created and then, for each date, an empty
    ## list is generated and filled with all the values.
    ## Then, the zip function creates the single dictionary of the date that
    ## is added to the final list.
    date_table = []
    for i in range(0, len(date_list)):
        value_list = []
        value_list.extend((date_id[i], date_list[i], date_day[i], date_month[i], date_year[i], date_quarter[i]))
        data_dict = dict(zip(date_header, value_list))
        date_table.append(data_dict)
    
    print('-> Date dictionary generated')
    return date_table

## With this function, given the list of dates and a single date,
## it returns the corresponding dateid
def getDateKey (date_table, date):
    for e in date_table:
        if e['date'] == date:
            return e['dateid']
    return str("NOTFOUND")

## This function creates the new two columns organization and organizationid.
## Organization contains the tuples of the three values needed to generate
## the table organization. 
## It returns the new list.
def generateOrganizationColumn (items):

    ## The name of the two columns are added at the end of the "header".
    items[0].append('Organization')
    items[0].append('organizationid')

    ## Then, the values of the three attributes of the organization are
    ## added in the list, for each row.
    for i in range(1, len(items)):
        items[i].append((items[i][10], items[i][11], items[i][12]))

    ## We order all the data by the elements of the new column.
    ## In this way, with the last for loop we can assign the organizationid
    ## in a faster way, without checking for all the rows each time.
    ## In particular, we check if the previous tuple is the same of the
    ## current one. If this is the case, we assign the same id. Otherwise,
    ## a new id is generated (using a counter).
    from operator import itemgetter
    items[1:] = sorted(items[1:], key=itemgetter(19))

    c = 1
    items[1].append(c)

    for i in range(1, len(items)-1):
        if items[i+1][19] == items[i][19]:
            items[i+1].append(c)
        else:
            c += 1
            items[i+1].append(c)
    
    print ('-> New column Organization added')
    return items

## The first parameter of this function is the list of dictionaries
## with all the records of the main csv file. The second one is the list
## of keys that need to be extracted from the main dictionaries to
## the new one (the new table).
## It returns the list of dictionaries.
def generateSingleTable (data_list, table_keys):
    table_list = []
    for i in range (0, len(data_list) - 1):
        current_record = {x:data_list[i][x] for x in table_keys}
        table_list.append(current_record)
    
    return table_list

## This function is used to generate all the tables, in form of list
## of dictionaries, following the attributes of the tables on the SQL
## server. First, it creates a list of dictionaries with all the records
## and then it separates this data in different table/list.
def generateTables (items):

    ## It extracts the list of attributes from the first row of
    ## the main list.
    header_list = items[0]
    
    ## Then, it creates the list of dictionaries with all the values
    ## from each record of the csv. With the zip function it assigns
    ## each value to its corresponding attribute (key).
    data_list = []

    for i in range(1, len(items)):
        value_list = items[i]
        data_dict = dict(zip(header_list, value_list))
        data_list.append(data_dict)

    ## We select all the attributes of each table and with the function
    ## 'generateSingleTable' all the tables (lists of dictionaries) are
    ## generated.
    answers_keys = ['AnswerId', 'QuestionId', 'UserId', 'AnswerValue', 'CorrectAnswer', 'iscorrect', 'Confidence', 'organizationid', 'DateAnswered', 'SubjectId']
    organization_keys = ['organizationid', 'GroupId', 'QuizId', 'SchemeOfWorkId']
    subject_keys = ['SubjectId']
    user_keys = ['UserId', 'Gender', 'RegionId', 'DateOfBirth', 'Region']
    geography_keys = ['Region', 'CountryCode', 'Continent']

    answers = generateSingleTable (data_list, answers_keys)
    organization = generateSingleTable (data_list, organization_keys)
    subject = generateSingleTable (data_list, subject_keys)
    user = generateSingleTable (data_list, user_keys)
    geography = generateSingleTable (data_list, geography_keys)

    print('-> ALL DICTIONARY TABLES GENERATED <-')
    return answers, organization, subject, user, geography

## Given the list of dictionaries and the attribute/key, this function
## generates a new list of dictionaries with a dictionary for each
## unique value of that specific key. In this way, it reduces the size of
## the list with only dictionaries with unique values.
def dictUniqueValues (table_list, attribute):
    print(f'-> Dictionary with unique values generated')
    return list({v[attribute]:v for v in table_list}.values())

## This function generates the ids for a list of dictionaries
## using a counter starting from the value 1.
## It returns the new list of dictionaries.
def generateIds (table_list, id_attribute):
    for i in range(0, len(table_list)):
        table_list[i].update({id_attribute:i+1})
    
    print(f"-> All {str(id_attribute)} generated")
    return table_list

## Given the dictionary of the table geography and a region,
## it returns the geoid of that region.
def getRegionKey (geography, region):
    for e in geography:
        if e['Region'] == region:
            return e['geoid']
    return str("NOTFOUND")

## Given the list of dictionaries, the table with all the dates 
## and the name of the attribute of the date and the one for 
## the new id, this function assigns for each record in the 
## dictionary the correct id for its date.
## It returns the new list of dictionaries.
def assignDateKey (table_list, date_table, date_attribute, id_attribute):
    print("Assigning all the date ids...")
    for i in range(0, len(table_list)):
        table_list[i][id_attribute] = (getDateKey(date_table, table_list[i][date_attribute][0:10]))
    
    print(f"-> All {id_attribute} assigned")
    return table_list

## As the previous function, this one assigns the correct id to
## each region (by name) in the table user.
## It returns the new list of dictionaries.
def assignRegionKey (table_list, geography_table, region_attr, id_attribute):
    print("Assigning all the region ids...")
    for i in range(0, len(table_list)):
        table_list[i][id_attribute] = (getRegionKey(geography_table, table_list[i][region_attr]))
    
    print(f"-> All {id_attribute} assigned")
    return table_list

### SUBJECT TABLE ###
## This function generate a list of dictionaries from the csv file
## of subjects. 
## It returns the list of dictionaries with all the subjects.
def generateSubjectDict (subject_csv):
    ## It creates the empty list and the list of the attributes of
    ## the database.
    subject_table = []
    subject_header = list(subject_csv[0])

    ## For each record it creates a dictionary that is added to the
    ## main list of subjects.
    for i in range(1, len(subject_csv)):
        curr_list = []
        curr_list.extend((subject_csv[i][0], subject_csv[i][1], subject_csv[i][2], subject_csv[i][3]))
        subject_dict = dict(zip(subject_header, curr_list))
        subject_table.append(subject_dict)
    
    print ('-> Subject dictionary generated')
    return subject_table

## The following four functions return the name, the id, the level
## or the parent id of a subject given the name or the id.
def getSubjectName (subject_table, subjectid):
    for e in subject_table:
        if e['SubjectId'] == subjectid:
            return e['Name']
    return str("NOTFOUND")

def getSubjectId (subject_table, subjectname):
    for e in subject_table:
        if e['Name'] == subjectname:
            return e['SubjectId']
    return str("NOTFOUND")

def getLevel (subject_table, subjectid):
    for e in subject_table:
        if e['SubjectId'] == subjectid:
            return e['Level']
    return str("NOTFOUND")

def getParent (subject_table, subjectid):
    for e in subject_table:
        if e['SubjectId'] == subjectid:
            return e['ParentId']
    return str("NOTFOUND")

## This function, given the dictionary of subject and the sequences of subjects
## for each answer record, creates a description that will be present in the
## final subject table. Each description is a string with the
## names of the subject present in the sequence, ordered by level (hierarchy)
## that is extracted from the dictionary. To create the string, this function
## extract the level of the subject and tries to put the name of that subject
## in an array, in the position matching the level. If that position is not
## empty, it tries to store the name in the next position until it founds
## an empty spot. Then, the string for that record is generated using the array
## with each name separated by a comma. This procedure is repeated for each
## record.
## It returns the list of sequences.
def generateSubjectList (subject_table, subject_dict):
    subject_ids_final = []

    for e in subject_dict:
        curr_dim = len(e['SubjectId'].replace(' ', '').strip('[]').split(','))
        array_subject_name = [None] * curr_dim

        for i in range (0, curr_dim):
            curr_level = int(getLevel(subject_table, e['SubjectId'].replace(' ', '').strip('[]').split(',')[i]))
            while array_subject_name[curr_level] != None:
                curr_level += 1
            array_subject_name[curr_level] = getSubjectName(subject_table, e['SubjectId'].replace(' ', '').strip('[]').split(',')[i])            
        
        subject_ids_final.append(', '.join(array_subject_name))
    
    return subject_ids_final

## Given the sequence of ids of subjects, this function returns the
## id assigned to that specific sequence.
def getDescriptionId (subject, subject_ids):
    for e in subject:
        if e['SubjectId'] == subject_ids:
            return e['subjectid']
    return str("NOTFOUND")

## This function assigns to each record of the list of dictionaries the
## correct id of the sequence of subject ids.
## It returns the new list of dictionaries.
def assignDescriptionKey (table_list, subject_table, subject_attribute, id_attribute):
    print("Assigning all the subject ids...")
    for i in range(0, len(table_list)):
        table_list[i][id_attribute] = (getDescriptionId(subject_table, table_list[i][subject_attribute]))
    
    print(f"-> All {id_attribute} assigned")
    return table_list

## Given the subject dictionary and the list of sequences of subjects,
## this functions adds the list to the dictionaries, one for each
## sequence.
def addSubjectDescriptions (subject, subject_ids):
    for i in range(0, len(subject)):
        subject[i].update({'description': subject_ids[i]})
    
    print('-> All descriptions assigned')
    return subject

### EXPORT TO CSV
## This function, given the list of dictionaries and the name of a key,
## removes that key (and its value) from each dictionary.
## It returns the new list of dictionaries.
def dropKey (table_list, key_toDrop):
    for e in table_list:
        e.pop(key_toDrop)
    
    print(f'-> Key {str(key_toDrop)} removed from the dictionary')
    return table_list

## With this function, the csv file is created from the list of 
## dictionaries.
def saveToCSV (table_list, file_dir):
    with open(file_dir, 'w', newline='') as file_csv:
        fields = list(table_list[0].keys())
        writer = csv.DictWriter(file_csv, fieldnames=fields)

        writer.writeheader()
        for e in table_list:
            writer.writerow(e)
    
    print(f'-> {file_dir} SAVED <-')