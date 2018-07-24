from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT

from security import authenticate, identity
from user import User,UserRegister
from item import Item, itemList

app = Flask(__name__)
app.secret_key = 'Deneme'

api = Api(app)


jwt = JWT(app,authenticate,identity)

          
api.add_resource(itemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(port=8080, debug=True)

