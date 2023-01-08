# simple script to load database with prodcuts 

from coffee_shop.models import Products
from coffee_shop import db
from main import app
import requests 
import json

with open("./product_data.json") as f: 
    prod_data = json.load(f)


with app.app_context():
    for prod in prod_data:
        product = Products(**prod)
        db.session.add(product)
        
    db.session.commit()

    