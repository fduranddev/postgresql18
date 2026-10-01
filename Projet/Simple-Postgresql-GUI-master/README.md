# User Friendly Postgresql Database GUI

A tkinter GUI with psycopg2 database adapter that runs the query and outputs info on the screen.
Useful for HR employees with no sql knowledge.

What it does: 
              
              - Display the database table.  - Sort by Name.
              - Insert data.                 - Sort by salary.
              - Update data.                 - Sort by job.
              - Delete data.                 - Search employee`s Name.           
              - Sort by ID.                  - Select data rows to edit.

### Requirements

- Python
- Tkinter module
- Psycopg2 module
- Re module

## Getting Started

Since this is a GUI to connect to a postgresql database you will need to have a postgresql database (You can use another 
sql language but you would need to change the adapter and tweak the code). 

Install Postgresql here: https://www.postgresql.org/

After finishing your postgre install go to the repository file postgresql_commands.py and on the first line:
   
    conn = psycopg2.connect(dbname='', host='', user='', password='')
   
Add your database name, host, user and password all inside quotes, by default your info should look like this:
             
    conn = psycopg2.connect(dbname='template0', host='localhost', user='postgres', password='Password you added on install')



### How to run it

We have two options on how to run it:
 
 1- The fast way is just opening the main_file.py on your IDE and running it 
(make sure both files are on the same folder).
 
 2- We can use pyinstaller to make a .exe file (this makes it better for 
the people that will constantly be using it, since after creating a .exe the 
only thing needed to run is to double click the file).

Lets make a .exe file. On your terminal type:

        pip install pyintaller
        
After installing pyinstaller go to the file directory on your terminal and type:

     pyinstaller --onefile -w main_file.py



## Using the GUI

Here are some examples with what you can do with the GUI:


- Inserting data

![inserting gif](https://user-images.githubusercontent.com/59767617/76035868-54d49980-5f21-11ea-8092-38c70984d106.gif)



- Deleting data

![delete gif](https://user-images.githubusercontent.com/59767617/76035898-69b12d00-5f21-11ea-83c4-5f7792aa7d18.gif)



- Updating data

![update gif](https://user-images.githubusercontent.com/59767617/76035926-7df52a00-5f21-11ea-8430-13952f71a55c.gif)



- Sorting data


![sort by gif](https://user-images.githubusercontent.com/59767617/76035955-906f6380-5f21-11ea-9d87-6a81a1e349cb.gif)



- Search data


![search name gif](https://user-images.githubusercontent.com/59767617/76035980-9feeac80-5f21-11ea-93a7-7550a7232c6b.gif)



- Error box

![Errors gif](https://user-images.githubusercontent.com/59767617/76035990-a41aca00-5f21-11ea-9549-eb41af34c78c.gif)










