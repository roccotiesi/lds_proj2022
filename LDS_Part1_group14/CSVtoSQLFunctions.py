###     CSV TO SQL  ###
###     GROUP_14    ###

### IMPORTING LIBRARIES
import csv
import pyodbc

### FUNCTIONS ###
##
## With the function csvToList we extract the content of the specific csv file into a list
## of dictionary that will be used for the operations in this file
def csvToList (file_dir):
    
    # It inizializes the list in which it will append the single dictionaries
    # Each dictionary contains a row of the csv with attributes as keys and the corrispondent
    # values
    list_from_csv = []

    # This operation accesses the csv file and put every row as a dictionary into the list
    with open(file_dir, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            list_from_csv.append(row)
    
    # The result of the function is the whole list
    print('-> CSV file to list done.')
    return list_from_csv

## With this function we get the list of the attributes of the table that will be used in the
## queries. We also create a list with "?" for each attribute that will be also used
## in the INSERT INTO query.
## It returns both lists.
def getAttributesList (list_csv):

    ## It extracts the keys from the first dictionary and creates the string
    attributes = list(list_csv[0].keys())

    ## It creates a list of "?", one for each attributes and then it creates
    ## the string with the join method
    attributes_dummy = []
    for i in attributes:
        attributes_dummy.append('?')

    print('-> Attributes of the list extracted.')
    return (attributes, attributes_dummy)

## This function renames all the keys of the dictionaries in lowercase because all the columns
## of the tables in the schema are lowercase while some attributes in the original csv are with
## uppercases. In this way, we automatically adapt all the names to the schema, except the ones
## that have totally different names (another function solves this problem).
## It returns the new list of dictionaries with the correct naming.
def renameKeysLower (list_csv, attributes):

    ## The parameters are the list of dictionaries and the list of the attributes to rename.
    ## With the following loop, we pass every value in a new key with only lowercase characters.
    for e in list_csv:
        for word in attributes:
            old_key = word
            new_key = old_key.lower()
            e[new_key] = e.pop(old_key)

    print('-> Renaming of the attributes completed.')
    return list_csv

## This function rename a specific key in every dictionary of the list.
## It returns the list with the correct key
def renameKey (list_csv, old_key, new_key):

    ## The parameters are the list, the old key to rename and the new name
    for e in list_csv:
        e[new_key] = e.pop(old_key)

    print('-> Renaming of', str(old_key), 'in', str(new_key), 'completed.')
    return list_csv

## This function casts all the values of the dictionaries in the correct types
## required before the import of the tables on the SQL server.
## A list of types is passed as a parameter with the correct order, following
## the order of the keys in the dictionary.
## It returns the list with the correct types.
def castValues (list_csv, type_list, attributes):
    for e in list_csv:
        ## for each dictionary in the list, it extracts the values
        ## as a new list. For each element of this list, it checks
        ## the type written in type_list and executes the casting.
        values_list = list(e.values())
        for i in range(0, len(values_list)):
            if type_list[i] == 'int':
                e[attributes[i]] = int(values_list[i])
            elif type_list[i] == 'float':
                e[attributes[i]] = float(values_list[i])

    print('-> Casting of all attributes types completed.')
    return list_csv

## The following functions are needed to correctly upload all
## the data on the SQL server.
## deleteTable executes the query to delete all the rows in
## a table, which name is passed as parameter.
## We added the [ ] to the query because using the word 'user'
## in queries could be problematic so in this way we specify
## that it refers to a table.
def deleteTableSQL (table_name, cnxn):
    cursor_del = cnxn.cursor()
    query = "DELETE from [" + str(table_name) + "]"
    print(query)
    cursor_del.execute(query)

    cnxn.commit()
    cursor_del.close()
    print('-> DELETE table completed')

def loadDataSQL (table_name, list_csv, attributes, attributes_dummy, cnxn):
    ## First step is to delete all the previous content in
    ## the table, to avoid errors with the primary keys
    deleteTableSQL(table_name, cnxn)

    ## The query is declared specifing the number of values to add
    ## for each row, using the notation '?'. The number of these values
    ## is computed by a previous function that returns the correct string
    ## of '?'s.
    ## Every 10000 records, a commit of the queries is executed.
    cursor = cnxn.cursor()
    query = "INSERT INTO [" + str(table_name) + "] (" + ', '.join(attributes) + ") VALUES("+ ', '.join(attributes_dummy) + ")"
    print(query)
    for i in range(len(list_csv)):
        rows = cursor.execute(query, (list(list_csv[i].values())))

        if i % 10000 == 0 and i > 0:
            cnxn.commit()
            print('---> Commit of ' + str(i) + ' records completed')

    cnxn.commit()
    cursor.close()
    print('-> Upload of table ' + str(table_name) + ' completed')

## With these functions, all the operations to prepare and then upload
## the data is performed, specifing the directory of the csv file and
## the name of the table on the server.
## The two operations are splitted because it could be necessary, for some
## tables, to perform also the renaming of one or more attributes.
def csvPreparation (file_dir):
    list_csv = csvToList(file_dir)
    attributes, attributes_dummy = getAttributesList(list_csv)
    list_csv = renameKeysLower(list_csv, attributes)

    return list_csv, attributes, attributes_dummy

def csvToSQL (table_name, list_csv, cnxn):
    attributes, attributes_dummy = getAttributesList(list_csv)
    loadDataSQL(table_name, list_csv, attributes, attributes_dummy, cnxn)

## This function delete all the records in all the tables.
## The order of the tables to delete is done to avoid any possible
## conflicts and problems with primary and foreign keys.
def deleteAllTables (cnxn):
    table_list = ['answers', 'user', 'date', 'geography', 'organization', 'subject']

    for e in table_list:
        deleteTableSQL (e, cnxn)