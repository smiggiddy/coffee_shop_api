from coffee_shop import create_app, db
from coffee_shop.models import Products
from flask_jwt_extended import create_access_token
import pytest 

def test_api_home(client):
    response = client.get("/api/v1/product-management")

    assert "prods" in response.json



def test_add_product(client, jwt_token):

    headers = {
        'Authorization': f'Bearer {jwt_token}'
    }    


    # Test adding a new drink product to the database
    data = {'product_name': 'Coca Cola', 'price': 2.99, 'size': 'L', 'qty': 10}
    response = client.post('/api/v1/product-management/drink', json=data, headers=headers)
    assert response.status_code == 201
    assert response.json == {'response': {'success': 'Added drink: Coca Cola to database.'}}

    # Test adding a product with the same name and size as an existing product
    data = {'product_name': 'Coca Cola', 'price': 2.99, 'size': 'L', 'qty': 10}
    response = client.post('/api/v1/product-management/drink', json=data, headers=headers)
    assert response.status_code == 409
    assert response.json == {'response': 'Error: Coca Cola, L is already in datebase.'}

    # Test adding a product with invalid data
    data = {'product_name': '', 'price': 2.99, 'size': 'L', 'qty': 10}
    response = client.post('/api/v1/product-management/drink', json=data, headers=headers)
    assert response.status_code == 400
    assert response.json == {'error': {'error': 'invalid product name'}}


def test_get_product_id(client, jwt_token, db_session):

    test_prod = {"product_name": "latte", "price": 4.75, "size": "M", "qty": 100 }

    prod = Products(**test_prod)
    db_session.add(prod)
    db_session.commit()

    name = 'latte'
    size = 'M'

    headers = {
        'Authorization': f'Bearer {jwt_token}'
    }
    response = client.post(f"/api/v1/product-management/{name}/{size}", headers=headers)

    assert response.status_code == 200
    assert response.json == {'product_id':  1}

    response = client.post("/api/v1/product-management/headass/sm", headers=headers)

    assert response.status_code == 409
    assert response.json == {'error': 'Invalid product name or size'}


