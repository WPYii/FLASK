from flask import Flask,jsonify,request,render_template
app = Flask(__name__)       # Create an obkect of Flask 

# @app.route('/')             # Creation of route for home page of the application 
# def home():
#     return "Hello,World!"

stores=[
    {
        'name' : 'My Wonderful Store',
        'items' : [
            {'name' : 'My Item',
             'price' : 15.99
            }
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

# Server's perspective
# POST - used to receive data
# GET  - used to send data back only

# POST /store data: {name}                      create new store with a given name
@app.route('/store', methods=['POST'])          # Define the route as '/store' and only accessible via POST request
def create_store():
    request_data=request.get_json()             # request is the request made by browser to this endpoint to create new store
                                                # get_json() converts JSON string to python dictionary
    new_store= {
        'name'  : request_data['name'],
        'items' : []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET  /store/<string:name>                     get a store for a given name and return some data
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name']==name:
            return jsonify(store)
        else:
            return jsonify({'message':'store not found!'})

# GET  /store                                   return a list of all the stores
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item {name: price}  create an item inside a specific store with a given name
@app.route('/store/<string:name>/item',methods=['POST'])
def create_item_in_store(name):
    request_data=request.get_json()             # request.get_json() converts the JSON object into Python data. 
    for store in stores:
        if store['name']==name:
            new_item={
                'name' : request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
        else:
            return jsonify({'message':'store not found'})

# GET  /store/<string:name>/item                get all the item in the specific store
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name']==name:
            return jsonify({'items':store['items']})
        else:
            return jsonify({'message':'store not found'})
app.run(port=5000)