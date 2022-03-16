import sqlite3
connection=sqlite3.connect('data.db')  # creating a connection object that represents the database. Data will store in "data.db"
cursor=connection.cursor()             # create a cursor
create_table="CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,username text,password text)" # "INTEGER PRIMARY KEY" is a built in way to auto increment values
cursor.execute(create_table)                                                                         # Create table users if it has not been created

create_table="CREATE TABLE IF NOT EXISTS items (name text, price real)" # "real" is number with decimal place
cursor.execute(create_table)                                            # Create table items if it has not been created               

connection.commit()
connection.close()