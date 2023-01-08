import datetime as dt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Products, OrderItems, Orders, Users
from .schemas import order_schema,orders_schema,product_schema,products_schema, users_schema
from . import db, limiter
from .helpers import *


api_views = Blueprint('api_views', __name__)

###### PRODUCTS ######
@api_views.route("/product-management")
@limiter.limit("30/minute")
def api_home():
    """Returns ALL product objects in database """

    try:
        products = Products.query.all()
        return jsonify(prods=[prod.to_dict() for prod in products ])
    except:
        return jsonify(error='Unable to process request')



@api_views.route("/product-management/<string:cat>", methods=['POST'])
@jwt_required()
def add_product(cat: str):
    """Adds new products based on cat """


    if request.is_json and cat == 'drink':
        data = request.get_json()

    elif request and cat == 'drink':
        data = request.get_data()
        data = request.get_data().decode()
        data = dict(item.split("=") for item in data.split("&"))

    error = product_validation(data)
    if error:
        return jsonify(error=error), 400

    product_name = data.get('product_name')
    size = data.get('size')

    try:  
        if not product_exists(product=product_name, size=size):
            product = Products(**data)

            db.session.add(product)
            db.session.commit()

            return jsonify(response={'success': f'Added {cat}: { product_name } to database.'}), 201
        else:
            return jsonify(response=f'Error: {product_name.title()}, {size} is already in datebase.'), 409
    
    except Exception as e:
        print(e)
        return jsonify(response={'Error': 'Invalid request for this page'}), 404





@api_views.route('/product-management/<string:name>/<string:size>', methods=['POST'])
@jwt_required()
def get_product_id(name: str, size: str):
    """Returns product_id based on name and size parameters"""
    id = _get_product_id(name, size)

    if id:
        return jsonify(product_id=id), 200

    else:
        return jsonify(error="Invalid product name or size"), 409


def _get_product_id(name, size):
    """Helper function to return product id"""
 
    prod_id = Products.query.filter_by(product_name=name, size=size).first()
    return prod_id.id if prod_id else None
    


@api_views.route("/product-management/<int:product_id>", methods=['PUT'])
@jwt_required()
def edit_product(product_id):
    """Method to edit products stored in the database"""

    db_commit_needed = False
    product = Products.query.filter_by(id=product_id).first()

    if product:
        if request.is_json:
            prod_data = request.get_json()
        else: 
            prod_data = request.get_data()

        new_product_name = prod_data.get('product_name', product.product_name)
        new_price = prod_data.get('price', product.price)
        new_size = prod_data.get('size', product.size)
        new_qty = prod_data.get('qty', product.stock_quanity)

        # checking to avoid dup size/prod names
        condition_one = new_product_name != product.product_name or new_size != product.size 

        if condition_one:
            if not product_exists(product=new_product_name, size=new_size):  
                product.product_name = new_product_name
                product.size = new_size
                
                db_commit_needed = True
            else:
                return jsonify(error="error updating product name or size already exists!"), 409


        condition_two = new_price != product.price or new_qty != product.stock_quanity

        if condition_two:
            product.price = new_price
            product.qty = new_qty  

            db.session.commit()
        elif db_commit_needed:
            db.session.commit()

        else:
            return jsonify(message="no parameteres needed an update."), 409
        
        return jsonify(message=f"Updated product {product.product_name}"), 202
    
    else:
        return jsonify(error="invalid product id or nothing to update"), 409


@api_views.route("/product-management/<int:prod_id>", methods=['DELETE'])
@jwt_required()
def delete_product(prod_id):
    """Method deletes product from db based on prod id"""

    #TODO may need to develop database management methods to handle orders if the product gets deleted

    prod = Products.query.filter_by(id=prod_id).first()

    if prod:
        prod_name = prod.product_name
        db.session.delete(prod)
        db.session.commit()
        return jsonify(message=f"{prod_id}: {prod_name} deleted from database."), 202
    else:
        return jsonify(error="invalid product id or resource doesn't exist"), 404


##### ORDERS ######
@api_views.route("/order-management")
@jwt_required()
def get_orders():
    """method returns db dump of all orders"""

    orders_list = Orders.query.all()
    orders_data = orders_schema.dump(orders_list)

    return jsonify(data=orders_data)


@api_views.route('/order-management', methods=['POST'])
@jwt_required()
def orders():
    """Method for placing orders"""

    order_total = ...
    
    if request.is_json:
        data = request.get_json()
    else:
        data = request.get_data()


    try: 
        order_name = data.get('order_name', 'system')
        order_email = data.get('order_email', 'test@example.org')
        order_date = dt.datetime.now().strftime("%d/%m/%Y") 
        order_total = data.get('order_total', 0)

        list_order_items = data.get('items_list', [{'item_id': 1, 'qty': 1, }])
        
        order = Orders(order_name=order_name, order_email=order_email, order_date=order_date, order_total=order_total)

        db.session.add(order)
        db.session.commit()

        # process order items

        for item in list_order_items:

            prod_id = item.get('item_id')
            qty = item.get('qty')
            order_item = OrderItems(
                item_id = prod_id,
                qty = qty,
                order_no = order.id 
            )
            db.session.add(order_item)
            order_total += product_price(prod_id=prod_id) * qty
            update_qty(prod_id=prod_id, qty=qty)

        
        order.order_total = order_total    
        db.session.commit()

        return jsonify({order_name: {'order_items': list_order_items}}), 201

    except Exception as e:
        print(e)
        return jsonify(error="invalid request. Please try again."), 409


@api_views.route("/order-management/<int:order_id>", methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    """Method deletes order from db based on order id"""

    #TODO may need to develop database management methods to handle orders if the product gets deleted

    order = Orders.query.filter_by(id=order_id).first()

    if order:
        order_name = order.order_name
        db.session.delete(order)
        db.session.commit()
        return jsonify(message=f"{order_id}: {order_name} deleted from database."), 202
    else:
        return jsonify(error="invalid product id or resource doesn't exist"), 404


##### AUTH ROUTES ########

@api_views.route("/auth/users", methods=['GET'])
@jwt_required()
def get_users():
    """returns all users in database"""

    users = Users.query.all()
    users = users_schema.dump(users)

    return jsonify(users=users)


@api_views.route("/auth/register", methods=['POST'])
def register():
    """Method to register access to API"""

    if request.is_json:
        data = request.json
    else:
        data = request.form

    email = data.get('email', None)

    account_exists = Users.query.filter_by(email=email).first()

    print(email, account_exists)

    if email and not account_exists:
        passwd = data.get('passwd')

        if _password_requirements(passwd=passwd):
            passwd = generate_password_hash(password=passwd, method='pbkdf2:sha256', salt_length=8)

            try:
                user = Users(email=email, password=passwd)

                db.session.add(user)
                db.session.commit()
                return jsonify(message=f'Success: created {email} API account'), 201

            except Exception as e:
                return jsonify(error=f'{e}')

        else:
            return jsonify(error='password does not meet complexity requirements'), 409   
    else:
        return jsonify(error="email exists or invalid data"), 409 

def _password_requirements(passwd):
    """Function returns true if password has min requirements"""
    pw_length = 8

    return len(passwd) >= pw_length
      



@api_views.route("/auth/login", methods=['POST'])
def login():
    """Method to authenticate to the API"""

    if request.is_json:
        data = request.get_json()
    else:
        data = request.get_data()

    if data:

        email = data.get('email')
        passwd = data.get('passwd')
    else:
        return jsonify(error='Invalid login request.')

  
    account_exists = Users.query.filter_by(email=email).first()
   

    if account_exists and check_password_hash(
            pwhash=account_exists.password,
            password=passwd
        ):

        access_token = create_access_token(identity=email)

        return jsonify(message='Login successful', access_token=access_token), 200
    else:
        return jsonify(message='Bad email or password entered'), 401



