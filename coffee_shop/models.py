from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import String, Column, Integer

class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)

    product_name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(2))
    qty = db.Column(db.Integer)


    def to_dict(self):
        # function returns store data in dictionary format
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True) 
    order_name = db.Column(db.String(250), nullable=False)
    order_email = db.Column(db.String(250), nullable=False)
    order_date = Column(String)

    # relationships
    order_items = relationship("OrderItems", back_populates="order")
    order_total = db.Column(db.Float, nullable=False)


class OrderItems(db.Model):
    __tablename__ = 'orderitems'
    id = db.Column(db.Integer, primary_key=True) 

    # order table 
    order_no = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = relationship("Orders", back_populates="order_items")

    # Product table 
    item = relationship("Products")
    item_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    qty = Column(Integer, nullable=False)


class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    


