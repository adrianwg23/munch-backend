from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String)

    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    restaurant = db.relationship("RestaurantModel")

    def __init__(self, item_name, restaurant_id):
        self.item_name = item_name
        self.restaurant_id = restaurant_id

    def json(self):
        return {"item_id": self.id, "restaurant_id": self.restaurant_id, "item_name": self.item_name}

    @classmethod
    def find_item_by_item_name(cls, item_name, restaurant_name):
        return cls.query.filter_by(restaurant_name=restaurant_name).filter_by(item_name=item_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()