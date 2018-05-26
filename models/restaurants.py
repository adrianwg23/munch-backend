from db import db


class RestaurantModel(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String, unique=True)

    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, restaurant_name):
        self.restaurant_name = restaurant_name

    def restaurants_json(self):
        return {"restaurant_id": self.id, "restaurant_name": self.restaurant_name,
                "items": [item.json() for item in self.items]}


    @classmethod
    def find_by_restaurant_name(cls, restaurant_name):
        return cls.query.filter_by(restaurant_name=restaurant_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
