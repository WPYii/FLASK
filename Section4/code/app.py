from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT,jwt_required
from security import authenticate, identity

app=Flask(__name__)
app.secret_key = 'Jose'
api=Api(app)

jwt=JWT(app,authenticate,identity)            # Create JWT object

items=[]

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field can't be left blank!"
    )
    @jwt_required()
    def get(self,name):                       # GET Request
        item=next(filter(lambda x : x['name'] == name,items),None)
        return {'item' : item}, 200 if item else 404

    def post(self,name):                      # POST Request
        data = Item.parser.parse_args()
        if next(filter(lambda x : x['name'] == name,items),None):
            return {'message' : "An item with name '{}' already exist".format(name)},400
        item={'name' : name, 'price' : data['price']}
        items.append(item)
        return item, 201

    def delete(self,name):
        global items
        items = list(filter(lambda x :x['name'] != name,items))
        return {'message' : 'Item deleted'}

    def put(self,name):
        data = Item.parser.parse_args()
        
        item = next(filter(lambda x : x['name'] == name,items),None)
        if item is None:
            item={'name' : name, 'price' : data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items' : items}

api.add_resource(Item,'/item/<string:name>')   # Tell our API that the resource is created, Item, now is accessible via our API
                                               # Creation of endpoint , no need use @app.route
api.add_resource(ItemList,'/items')
app.run(port=5000,debug=True)


