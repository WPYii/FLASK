from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.information import InformatonList
from resources.information import Information
from security import authenticate, identity
from resources.user import UserRegister

appLogin=Flask(__name__)
appLogin.secret_key="poyi"
api=Api(appLogin)

jwt = JWT(appLogin,authenticate,identity)

api.add_resource(UserRegister,'/register')
api.add_resource(Information,'/info/<string:name>')
api.add_resource(InformatonList,'/allinfo')

if __name__ == '__main__':
    appLogin.run(port=5000,debug=True)
    