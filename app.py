from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Deneme'

api = Api(app)


jwt = JWT(app,authenticate,identity)

items = []

class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item" : item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return {"message":"An item wit name '{}' already exists".format(name)}
        data = request.get_json()
        item = {"name" : name, "price" : data['price']}
        items.append(item)   
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message" : "item deleted"}
    
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("price",
            type=float,
            required=True,
            help="This field cannot be left blank"
        )
        data = parser.parse_args()
        
        data = request.get_json()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name" : name, "price":data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item


class itemList(Resource):
    def get(self):
        return {"items": items}
        
        
api.add_resource(itemList, '/items')
api.add_resource(Item, '/item/<string:name>')

app.run(port=8080, debug=True)
