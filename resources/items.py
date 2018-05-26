from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.items import ItemModel

parser = reqparse.RequestParser()
parser.add_argument("item_name", type=str, required=True)
parser.add_argument("restaurant_name", type=str, required=True)


class NewItem(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        item = ItemModel(**data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred saving the item."}, 500

        return item.json(), 201


class ItemOrder(Resource):
    def post(self):
        data = parser.parse_args()
        item = ItemModel.find_item_by_item_name(**data)

        if item is None:
            return {"message": "Item or restaurant does not exist"}

        return {"message": "Success"}


