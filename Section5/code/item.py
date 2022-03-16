from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()                                   # Create parser
    parser.add_argument('price',                                        # Required argument for users to enter
        type=float,
        required=True,
        help="This field can't be left blank!"
    )
    @jwt_required()                                                     # Authentication is required for this "get" method    
    def get(self,name):                                                 # GET Request  
        item = self.find_by_name(name)                                                     
        if item is not None:
            return item
        else:
            return {'message' : 'Item not found'},404

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"                       # "WHERE" means its filtering the results, it is a search condition. For this example,
                                                                         # will only select rows where "name" matches a parameter  
                                                                         # "?" means any parameter
        result=cursor.execute(query,(name,))                             # Pass in a parameter (name,) so "name" in "name=?" will have a value
        row = result.fetchone()                                          # Fetches the next row of a query result set, returning a single sequence, or None when no more data is available.
        connection.close()                                               # Get the first row out of the result set

        if row is not None:                                              # If there is row. row[0] is "name", row[1] is "price"
            return {'item' :{'name' : row[0],'price' : row[1]}}          # return the json

    def post(self,name):                                                                 # POST Request
        if Item.find_by_name(name):                                                      # Check if item is in the database, can also write "self.find_by_name(name)"
            return {'message' : "An item with name '{}' already exist".format(name)},400
        data = Item.parser.parse_args()                                                  # If not in database,received the data from json payload and parse to "data"
        item={'name' : name, 'price' : data['price']}

        try:
            self.insert(item)                                              # Call the "insert" mtehod and pass the "item" to the "insert" method
        except:
            return {"message" : "An error occured inserting the item"},500 # Except block only runs when there is error, 500 is internal server error
        
        return item, 201

    @classmethod
    def insert(cls,item):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="INSERT INTO items VALUES (?,?)"               # insert values for rows for table "items", "?" means any parameter
        cursor.execute(query,(item['name'],item['price']))   # (item['name'],item['price']) corresponds to (?,?) and will be inserted into row of table "items"
        connection.commit()
        connection.close()

    def delete(self,name):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="DELETE FROM items WHERE name=?"              # delete row from table "items" where "name" matches a parameter, "?" means any parameter
        cursor.execute(query,(name,))                       # Pass in a parameter (name,) so "name" in "name=?" will have a value
        connection.commit()
        connection.close()
        return {'message' : 'Item deleted'}

    def put(self,name):
        data = Item.parser.parse_args()     # received data from json payload and parse to "data"
        
        item = Item.find_by_name(name)      # or can write "self.find_by_name"
        updated_item={'name' : name, 'price' : data['price']}
        if item is None:                    # if the item wasnt found on the database
            try:
                Item.insert(updated_item)   # or can write "self.insert(updated_item)"        
            except:
                return {"message" : "An error occurred insrting the item"},500 
        else:
            try:
                self.update(updated_item)
            except:
                return {"message" : "An error occurred updating the item"},500
        return updated_item

    @classmethod
    def update(cls,item):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="UPDATE items SET price=? WHERE name=?"      # This will set every price in the table to the value of "?" parameter where the name equals to the value of "?" parameter
        cursor.execute(query,(item['price'],item['name'])) # For this case, the "?" in "price=?" is equal to "item['price']"
        connection.commit()                                # the "?" in "name=?" is equal to "item['name'}"
        connection.close()

class ItemList(Resource):
    def get(self):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="SELECT * FROM items"         # This will select everythig from the items table
        result=cursor.execute(query)        
        items=[]
        for row in result:
            items.append({'name': row[0],'price':row[1]})
        connection.close()
        return {'items' : items}            # Return the list items