from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity  # Import functions "authenticate" and "identity" from "Security" script that is in the same folder
from resources.user import UserRegister      # Tell python to look into "resources" folder to look for "user"  script and import class "UserRegister"
from resources.item import Item,ItemList     # Tell python to look into "resources" folder to look for "item"  script and import class "Item","ItemList"
from resources.store import Store,StoreList  # Tell python to look into "resources" folder to look for "store" script and import class "Store","StoreList"
from db import db

app=Flask(__name__)                                         # Must include
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'   # SQLAlchemy database will live at the root folder of our project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        # Ask SQLAlchemy not to track any changes in modification    
app.secret_key = 'Jose'                                     # Set a complicated key
api=Api(app)                                                # (name_of_the_python_file)

@app.before_first_request     # this method will run before the first request into this app
def create_tables():          # this will create the "data.db" file, the name of the table is specified in line 10
    db.create_all()     

jwt=JWT(app,authenticate,identity)             # Create JWT object

api.add_resource(Item,'/item/<string:name>')   # Tell our API that the resource is created, Item, now is accessible via our API
                                               # Creation of endpoint , no need use @app.route
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')

if __name__ == '__main__':                     # If we run this python file, __name__ will be equal to __main__. 
                                               # If we import this pyhotn file, __name__ will not be equal to __main__
    db.init_app(app)                           # This callback can be used to initialize an application for the use with this database setup. 
                                               # inside "()" is the name of the python file
    app.run(port=5000,debug=True)              # Must include


