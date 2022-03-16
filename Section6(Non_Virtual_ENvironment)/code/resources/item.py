from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel                                       # imported "ItemModel" class of "item.py" from "models" folder. So we 
                                                                        # can use the methods inside.

class Item(Resource):
    parser = reqparse.RequestParser()                                   # Create parser
    parser.add_argument('price',                                        # Required argument for users to enter
        type=float,
        required=True,
        help="This field can't be left blank!"
    )
    parser.add_argument('store_id',                                     # Required argument for users to enter
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    @jwt_required()                                                     # Authentication is required for this "get" method    
    def get(self,name):                                                 # GET Request  
        item = ItemModel.find_by_name(name)                             # "item" is an object instead of dictionary now                                     
        if item is not None:
            return item.json()                                          # Using the json() method in "item.py" of "models" folder. to return JSON representation
                                                                        # "item" is object, we need to change to json for representation using "json()"
        else:
            return {'message' : 'Item not found'},404

    def post(self,name):                                                                 # POST Request
        if ItemModel.find_by_name(name):                                                 # Check if item is in the database, can also write "self.find_by_name(name)"
            return {'message' : "An item with name '{}' already exist".format(name)},400
        data = Item.parser.parse_args()                                                  # If not in database,received the data from json payload and parse to "data"
                                                                                         # The data received are "price" and "store_id"
        item=ItemModel(name, data['price'],data['store_id'])

        try:
            item.save_to_db()                                             
        except:
            return {"message" : "An error occured inserting the item"},500               # Except block only runs when there is error, 500 is internal server error
        
        return item.json(), 201

    def delete(self,name):
        item=ItemModel.find_by_name(name)
        if item is not None:
            item.delete_from_db()
        else:
            return {'message' : "Item deleted"}

    def put(self,name):
        data = Item.parser.parse_args()         # received data from json payload and parse to "data"
                                                # The data received are "price" and "store_id"
        
        item = ItemModel.find_by_name(name)     # or can write "self.find_by_name"

        if item is None:                        # if the item wasn't found on the database
            item=ItemModel(name,data['price'],data['store_id'])  # Creating a new object
        else:
            item.price=data['price']            # if the item exists, update the price using the value from "data"
        item.save_to_db()                       # SQLAlchemy will convert object to dictionary for us
        return item.json()                      # "item" is object, we need to change to json for representation using "json()"

class ItemList(Resource):
    def get(self):
        return {'items' : [item.json() for item in ItemModel.query.all()]}    # ".all()" returns all of the object in database