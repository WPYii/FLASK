import imp
import sqlite3
from db import db

class UserModel(db.Model):                          # extend "db.Model" will tell the SQLAlchemy that this class "UserModel" are things we are going to be saving to database or retrieving from database
    __tablename__ ='users'                          # Tell SQLAlchemy the table name where these models are going to be saved. For this case, table name is "users"
    id = db.Column(db.Integer,primary_key=True)     # Specify what columns we want the table to contain. There's a column called "id" of type "Integer" and its a "primary_key"
                                                    # Primary key means its unique number
    username = db.Column(db.String(80))             # Sprcify column called "username" of type "String" and is maximum 80 characters 
    password = db.Column(db.String(80))             # Sprcify column called "password" of type "String" and is maximum 80 characters 
                                                    # The above codes we told SQLAlchemy the 3 columns that this model will have. When saving to database, it will only look for these 3 parameters
                                                    # id, username and password
    def __init__(self,username,password):                 
        self.username   = username                  # "self.username" and "self.password" must match with the codes above for it to store them into database
        self.password   = password

    def save_to_db(self):
        db.session.add(self)    
        db.session.commit()

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()   # "cls.query" is essentially equal to "SELECT * FROM users"
                                                                # "cls.query.filter_by(username=username).first()" equals to "SELECT * FROM users WHERE username=username LIMIT 1"
                                                                # The second "username" is from the argument
                                                                # ".first()" means first row
                                                                # SQLAlchemy will convert the row to object, so for this classmethod, will return
                                                                # object "UserModel" that have "self.username" and "self.password"
    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()