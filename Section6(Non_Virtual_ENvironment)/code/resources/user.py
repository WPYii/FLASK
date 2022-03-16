from importlib.resources import Resource
from multiprocessing import connection
import sqlite3                                  # By importing sqlite3, the entire code is able to interact with SQLite                                   
from flask_restful import Resource,reqparse
from models.user import UserModel

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
        data = UserRegister.parser.parse_args()                                 # Received the data from the JSON payload and parse to "data"
        if UserModel.find_by_username(data['username']) is not None:            # Check the username entered with the find_by_username methods in class USER to check if the username is it already in database
            return {"message" : "A user with that username already exists"},400 # Can also write as "self.find_by_username(data['username'])"

        user=UserModel(data['username'],data['password'])                       # Creating new object if its a newly register username   
        user.save_to_db()                                                       # SQLAlchemy will convert object to dictionary for us
        return {"message" : "User created sucessfully"},201

    


