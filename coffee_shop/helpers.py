from .models import *


def product_validation(data):
    """validates data in product is accurate"""

    product_name = data.get('product_name')
    price = data.get('price')
    size = data.get('size')
    qty = data.get('qty')

    # validate the data

    if float(price) < 0 or type(price) != float or not price:
        return {'error': 'invalid price'} 
    
    if int(qty) < 0 or type(qty) != int or not qty:
        return {'error': 'invalid qty'}

    # ensure size is in uppercase and create size ranges
    prod_sizes = ['XL', 'L', 'M', 'S']

    if size not in prod_sizes or not size:
        return {'error': 'invalid product size'} 

    if not product_name or not product_name:
        return {'error': 'invalid product name'}


def product_exists(product, size):
    """BOOL helper function checks product name/size in database"""

    prod_exists = Products.query.filter_by(product_name=product, size=size).first()

    return prod_exists != None


def product_price(prod_id):
    """Helper function returns product price"""
    prod = Products.query.filter_by(id=prod_id).first()

    return prod.price if prod else 0 


def update_qty(prod_id, qty):
    """helper function updates quanity in product table """

    prod = Products.query.filter_by(id=prod_id).first()

    prod.qty -= qty 

    return f'Updated {prod.product_name}\'s qty: {prod.qty}'