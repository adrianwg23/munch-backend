from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.restaurants import RestaurantModel


parser = reqparse.RequestParser()
parser.add_argument("restaurant_name", type=str, required=True, help="This field cannot be blank.")


class NewRestaurant(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()

        if RestaurantModel.find_by_restaurant_name(data["restaurant_name"]):
            return {"message": "This restaurant already exists"}, 400

        restaurant = RestaurantModel(data["restaurant_name"])
        try:
            restaurant.save_to_db()
            return {"restaurant_id": restaurant.id}, 201
        except:
            return {"message": "An error occurred creating the restaurant"}, 500


class Restaurants(Resource):
    def get(self):
        return {"restaurants": [restaurant.restaurants_json() for restaurant in RestaurantModel.query.all()]}