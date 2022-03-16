from db import db

class StoreModel(db.Model):                     # extend "db.Model" will tell the SQLAlchemy that this class "ItemModel" are things we are going to be saving to database or retrieving from database
    __tablename__ = 'stores'                    # Tell SQLAlchemy the table name where these models are going to be saved. For this case, table name is "items"
    id = db.Column(db.Integer,primary_key=True) # Specify what columns we want the table to contain. There's a column called "id" of type "Integer" and its a "primary_key"
    name = db.Column(db.String(80))             # Sprcify column called "name" of type "String" and is maximum 80 characters 
    items=db.relationship('ItemModel' , lazy = 'dynamic') # Specify there is a relationship with 'ItemModel"
                                                          # allows a store to see which items are in the "items" table with the "store_id" equal to its own "id"
                                                          # The variable "items" is a list of item models, many to one relationship
                                                          # "lazy = 'dynamic"
    def __init__(self,name):
        self.name  = name                       # "self.name" and "self.price" must match with the codes above for it to store them into database
    
    def json(self):
        return {'name' : self.name, 'items' : [item.json() for item in self.items.all()]}
        
    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()  # this code equals to "SELECT * FROM items WHERE name=name LIMIT 1" The second "name" is from the argument
                                                       # ".first()" means only return the first row
                                                       # Will look for table "users" coz already specified in line 4
                                                       # SQLAlchemy will convert the row to object, so for this classmethod, will return
                                                       # object "ItemModel" that have "self.name" and "self.price"
    def save_to_db(self):
        db.session.add(self)        # The "session" is a collection of objects that we want to write to the database. 
                                    # Can add multiple objects to the session and add them all at once
                                    # SQLAlchemy can convert objects to rows, thus we do not need to specify which row data to insert
                                    # just need to insert the object to the database
        db.session.commit()         # Saved to the database

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()