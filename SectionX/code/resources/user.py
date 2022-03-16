from flask_restful import Resource,reqparse
from multiprocessing import connection
import sqlite3
from models.user import UserModel

class UserRegister(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True,help="Mandatory section")
    parser.add_argument('password',type=str,required=True,help="Mnadatory section")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']) is not None:
            return {'massage' : 'A user with that username is already exists'},400
        else:
            connection=sqlite3.connect('data.db')
            cursor=connection.cursor()
            query="INSERT INTO users VALUES (NULL,?,?)"
            cursor.execute(query,(data['username'],data['password']))
            connection.commit()
            connection.close()
            return {'message' : 'User created sucessfully!'},201
