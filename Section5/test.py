import sqlite3

connection =sqlite3.connect('data.db') # Initialize connection,create a folder called 'data.db' inside our current directory as sqlite database
cursor = connection.cursor()           # Similar to mouse cursor, allow you to select things and start things
create_table = "CREATE TABLE users (id int, username text ,password text)" # Created table called users with 3 columns, id, username and password
cursor.execute(create_table)

user = (1,'jose','asdf')
insert_query = "INSERT INTO users VALUES (?,?,?)" # "INSERT INTO" the table we want to insert into, which is "users". Text after "VALUES" 
                                                  # are the values we want to insert into the table
cursor.execute(insert_query,user)                 # Run the query with the cursor

user1=[
    (2,'rolf','asdf'),
    (3,'anne','xyz')
]
cursor.executemany(insert_query,user1)            # "users" here is the entry we want to insert to the table

select_query="SELECT * FROM users"                # "SELECT * From users", "*"" means all the columns, "users" means the table we want to extract entries
# print(list(cursor.execute(select_query)))
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()