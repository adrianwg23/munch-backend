from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.items import ItemModel
from models.restaurants import RestaurantModel

parser = reqparse.RequestParser()
parser.add_argument("item_name", type=str, required=True)
parser.add_argument("restaurant_name", type=str, required=True)


class NewItem(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        item_name = data["item_name"]
        restaurant_name = data["restaurant_name"]
        restaurant = RestaurantModel.find_by_restaurant_name(restaurant_name)
        item = ItemModel(item_name, restaurant.id)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred saving the item."}, 500

        return item.json(), 201


class ItemOrder(Resource):
    def post(self):
        data = parser.parse_args()
        item_name = data["item_name"]
        restaurant_name = data["restaurant_name"]
        restaurant = RestaurantModel.find_by_restaurant_name(restaurant_name)
        item = ItemModel.find_item_by_item_name(item_name, restaurant.id)

        if item is None:
            return {"message": "Item or restaurant does not exist"}
        else:
            item.ordered = True
            item.save_to_db()

        return {"message": "Success"}


class ItemOrderList(Resource):
    def get(self, restaurant_id):
        ordered_items =[]
        for item in ItemModel.query.filter_by(restaurant_id=restaurant_id).all():
            if item.is_item_ordered():
                ordered_items.append(item)

        return {"ordered_items": [item.json() for item in ordered_items]}, 404


