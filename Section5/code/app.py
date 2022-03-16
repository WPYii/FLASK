from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT,jwt_required
from security import authenticate, identity
from user import UserRegister
from item import Item,ItemList

app=Flask(__name__)                                                     # Must include
app.secret_key = 'Jose'                                                 # Set a complicated key
api=Api(app)                                                            # (name_of_the_python_file)

jwt=JWT(app,authenticate,identity)                                      # Create JWT object

api.add_resource(Item,'/item/<string:name>')   # Tell our API that the resource is created, Item, now is accessible via our API
                                               # Creation of endpoint , no need use @app.route
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':                     # If we run this python file, __name__ will be equal to __main__. 
                                               # If we import this pyhotn file, __name__ will not be equal to __main__
    app.run(port=5000,debug=True)              # Must include




