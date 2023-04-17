# Laboratory of Data Science | Project 
### University of Pisa - A.Y. 2022-23


## Authors

- Rocco Tiesi [@roccotie](https://www.github.com/roccotie)
- Lorenzo Pieri [@lorenzopieri99](https://www.github.com/lorenzopieri99)


## Description
The project was a crucial component of the Laboratory of Data Science course, which is part of the Master's Degree in Data Science and Business Informatics at the University of Pisa. This course provided a comprehensive introduction to various techniques and tools used in Business Informatics, such as data integration, OLAP cube construction, MDX querying, and data visualization with Power BI. 
### Part 1: Data Integration
In this part of the project, we used Python to perform data cleaning, transformation, and loading of a provided CSV dataset into a SQL database. We were not allowed to use any additional libraries (e.g. pandas), so we had to write our own code to handle data processing tasks. The goal was to create a clean and structured database that could be easily queried and analyzed in later stages of the project.

#### Assignment 0
The schema was reproduced using SQL Server Management Studio and uploaded to the university's department server.

#### Assignment 1
A Python script was written to create six tables in the data warehouse from the answers_full CSV file. The program performed various data processing tasks, such as adding a continent column, generating a dictionary of country codes and names, and creating tables for organizations, subjects, and dates. 

#### Assignment 2
A second Python script was written to populate the database with the data prepared in Assignment 1. The program extracted the content of a file and put it into a list of dictionaries, renamed the keys to lowercase (to match the names provided by the mandatory schema), and uploaded the data into the corresponding tables on the server.
### Part 2: SSIS Solutions
SQL Server Integration Services (SSIS) is used to solve some queries on the database created in Part 1. Three assignments are completed, each with a SSIS package.

#### Assignment 0
For every subject, the number of correct answers of male and female students.

#### Assignment 1
A subject is said to be easy if it has more than 90% correct answers, while it is said to be hard if it has less than 20% correct answers. List every easy and hard subject, considering only subjects with more than 10 total answers.

#### Assignment 2
For each country, the student or students that answered the most questions correctly for that country.

### Part 3: Multidimensional Data Analysis
MultiDimensional eXpression (MDX) is used in SQL Management Studio to answer business questions on a datacube that is constructed based on the previously created database. Power BI is also employed to develop a dashboard for showing some distributions of the data.
#### Assignment 0
We used Visual Studio with the Analysis services tool to connect to the database and create the datacube, establishing dimensions and measures.
#### Assignment 1
The student who made the most mistakes for each country is calculated. The TOPCOUNT, NONEMPTY, and GENERATE functions were used to accomplish this task.

#### Assignment 2
The student with the highest total correct answers for each subject was shown. The member MaxCorrect and the FILTER function were used to obtain the desired results.

#### Assignment 3
The student with the highest ratio between their total correct answers and the average correct answers of that continent was calculated. A member AvgCorrect was created to compute the average, and another member Ratio was created to compute the ratio. The TOPCOUNT and GENERATE functions were used to select the desired results.

#### Assignment 4
A dashboard was developed to show the geographical distribution of the answers. A map and a bar plot were used to represent the correct and wrong answers for each country and region.

#### Assignment 5
Three kinds of plots focusing on the gender of the students and the subjects were implemented. Two plots were used to show the distribution of correct and wrong answers and the number of total answers and students for each subject, and another plot was used to show the distribution of correct answers by birth year and gender.
