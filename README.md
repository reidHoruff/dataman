##dataman.py

##About
dataman is a small python script that extends the functionality of manage.py to aid in the development of django web apps.  
All necessary info about the database and app are read from the django project's settings.py file.

##Usage
`help` displays help message  
`--dump` dumps projects mySQL database to dbname-month-day-year-hour-minute.sql  
`--dump [filename.sql]` dumps database to specified SQL file  
`--restore [filename.sql]` restores project's database from SQL dump  
`--clear` clears data from project's database, keeps tables and colums names  
`--create` creates database for project  
`--drop` drops project's SQL database  
`--sync` same as `manage.py syncdb` except creates database if does not already exist  

##Restrictions
Currently only supports mySQL configurations.

