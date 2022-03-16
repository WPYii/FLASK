from importlib.resources import Resource
from multiprocessing import connection
import sqlite3                                      # By importing sqlite3, the entire code is able to interact with SQLite
from flask_restful import Resource,reqparse

class User:
    def __init__(self,_id,username,password):
        self.id         = _id
        self.username   = username
        self.password   = password

    @classmethod
    def find_by_username(cls,username):
        connection=sqlite3.connect('data.db')        # Connect to database "data.db"
        cursor=connection.cursor()                   
        query="SELECT * FROM users WHERE username=?" # "WHERE" means its filtering the results, it is a search condition. For this example,
                                                     # will only select rows where "username" matches a parameter
                                                     # "?" means any parameter
        result=cursor.execute(query,(username,))     # Pass in a parameter (username,) so "username" in "username=?" will have a value
        row = result.fetchone()                      # Fetches the next row of a query result set, returning a single sequence, or None when no more data is available.
                                                     # Get the first row out of the result set
        if row is not None:
            user = cls(row[0],row[1],row[2])         # If there is row, we create user object using data from that role. row[0] is first column...
        else:                                        # instead of cls(row[0],row[1],row[0]), we can use cls(*row)
            user=None
        connection.close()
        return user
    
    @classmethod
    def find_by_id(cls,_id):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="SELECT * FROM users WHERE id=?"  # "WHERE" means its filtering the results, it is a search condition. For this example,
                                                # will only select rows where "id" matches a parameter
                                                # "?" means any parameter
        result=cursor.execute(query,(_id,))     # Pass in a parameter (_id,) so "id" in "id=?" will have a value
        row = result.fetchone()                 # Fetches the next row of a query result set, returning a single sequence, or None when no more data is available.
                                                # Get the first row out of the result set
        if row is not None:
            user = cls(row[0],row[1],row[2])    # If there is row, we create user object using data from that role. row[0] is first column...
        else:                                   # instead of cls(row[0],row[1],row[0]), we can use cls(*row)
            user=None
        connection.close()
        return user

class UserRegister(Resource):   
    parser = reqparse.RequestParser()           # Create parser
    parser.add_argument('username',             # Required argument for users to enter
        type=str,
        required=True,
        help="This field cnanot be blank"
    )
    parser.add_argument('password',             # Required argument for users to enter
        type=str,
        required=True,
        help="This field cnanot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()                     # Received the data from the JSON payload and parse to "data"
        if User.find_by_username(data['username']) is not None:     # Check the username entered with the find_by_username methods in class USER to check if the username is it already in database
            return {"message" : "A user with that username already exists"},400 # Can also write as "self.find_by_username(data['username'])"

        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        query= "INSERT INTO users VALUES (NULL,?,?)"                # The id will be auto-incrementing so we put "NULL"
        cursor.execute(query,(data['username'],data['password']))

        connection.commit()
        connection.close()
        return {"message" : "User create sucessfully"},201

    


