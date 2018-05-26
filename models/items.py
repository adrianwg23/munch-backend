from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String)

    restaurant_name = db.Column(db.Integer, db.ForeignKey("restaurants.restaurant_name"))
    user = db.relationship("RestaurantModel")

    def __init__(self, item_name, restaurant_name):
        self.item_name = item_name
        self.restaurant_name = restaurant_name

    def json(self):
        return {"item_id": self.id, "restaurant_name": self.restaurant_name, "item_name": self.item_name}

    @classmethod
    def find_item_by_item_name(cls, item_name, restaurant_name):
        return cls.query.filter_by(restaurant_name=restaurant_name).filter_by(item_name=item_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()