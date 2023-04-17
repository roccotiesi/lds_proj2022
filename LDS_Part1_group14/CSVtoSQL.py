from CSVtoSQLFunctions import *

server = 'tcp:lds.di.unipi.it' 
database = 'group_14_DB' 
username = 'group_14' 
password = '0YWVIPJN' 
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password
cnxn = pyodbc.connect(connectionString)

deleteAllTables (cnxn)

### IMPORT GEOGRAPHY TABLE
geo_list, attributes, attributes_dummy = csvPreparation ('geo_final.csv')
geo_list = renameKey(geo_list, 'countrycode', 'country_name')
csvToSQL ('geography', geo_list, cnxn)

### IMPORT DATE TABLE
date_list, attributes, attributes_dummy = csvPreparation ('date_final.csv')
csvToSQL ('date', date_list, cnxn)

### IMPORT USER TABLE
user_list, attributes, attributes_dummy = csvPreparation ('user_final.csv')
csvToSQL ('user', user_list, cnxn)

### IMPORT ORGANIZATION TABLE
org_list, attributes, attributes_dummy = csvPreparation ('org_final.csv')
csvToSQL('organization', org_list, cnxn)

### IMPORT SUBJECT TABLE
subj_list, attributes, attributes_dummy = csvPreparation ('subject_final.csv')
csvToSQL('subject', subj_list, cnxn)

### IMPORT ANSWERS TABLE
answers_list, attributes, attributes_dummy = csvPreparation ('answers_final.csv')
answers_list = renameKey(answers_list, 'answervalue', 'answer_value')
answers_list = renameKey(answers_list, 'correctanswer', 'correct_answer')
csvToSQL('answers', answers_list, cnxn)

cnxn.close()