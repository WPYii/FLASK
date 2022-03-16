from importlib.resources import Resource
from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store is not None:
            return store.json() # gonna try this later StoreModel.json(store)
        else:
            return {'message' : 'Store not found'}, 404

    def post(self,name):
        if StoreModel.find_by_name(name) is not None:
            return {'message' : "A store with name '{}' already exists.".format(name)},400
        else:
            store=StoreModel(name)
            try:
                store.save_to_db()
                return store.json(),201
            except:
                return {'message' : 'An error occurred while creating the store'},500      
         

    def delete(self,name):
        store = StoreModel.find_by_name(name) 
        if store is not None:
            store.delete_from_db()
        else:
            return {'message' : 'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores' : [store.json() for store in StoreModel.query.all()]}    # ".all()" returns all of the object in database