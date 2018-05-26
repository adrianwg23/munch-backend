import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.items import NewItem, ItemOrder
from resources.restaurants import NewRestaurant, Restaurants
from resources.user import UserRegister, UserLogin, UserList

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.config["JWT_SECRET_KEY"] = '\x9a\xf5\xba.qTE<e\xd2\xd4\x1c\x13\xa2\x83\x8a\x90\xbb\xfe\xb5%\xd0\xa1#'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
jwt = JWTManager(app)


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(NewItem, "/item/new")
api.add_resource(ItemOrder, "/item/order")
api.add_resource(NewRestaurant, "/restaurant/new")
api.add_resource(Restaurants, '/restaurants')
api.add_resource(UserList, "/users")


if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
