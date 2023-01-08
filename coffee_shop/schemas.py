from . import ma

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'product_name', 'price', 'size','stock_quantity')


class OrdersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'order_name', 'order_email', 'order_total', 'order_date', 'order_total')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password')


order_schema = OrdersSchema()
orders_schema = OrdersSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
    