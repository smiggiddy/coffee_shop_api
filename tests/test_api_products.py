from coffee_shop import create_app, db
from coffee_shop.models import Products
from flask_jwt_extended import create_access_token


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

    headers = {'Authorization': f'Bearer {jwt_token}'}

    # testing with empty database 
    name = 'headass'
    size = 'L'
    response = client.post(f"/api/v1/product-management/{name}/{size}", headers=headers)

    assert response.status_code == 409
    assert response.json == {'error': 'Invalid product name or size'}


    test_prod = {"product_name": "latte", "price": 4.75, "size": "M", "qty": 100 }

    prod = Products(**test_prod)
    db_session.add(prod)
    db_session.commit()

    name = 'latte'
    size = 'M'

    response = client.post(f"/api/v1/product-management/{name}/{size}", headers=headers)

    assert response.status_code == 200
    assert response.json['product_id'] == 1

    name = 'headass'
    size = 'L'
    response = client.post(f"/api/v1/product-management/{name}/{size}", headers=headers)

    assert response.status_code == 409
    assert response.json == {'error': 'Invalid product name or size'}

    # testing with empty params

    name = ''
    size = ''
    response = client.post(f"/api/v1/product-management/{name}/{size}", headers=headers)

    assert response.status_code == 404
    assert response.json == {'error': 'Invalid API request'}

    # testing invalid paramaters 
    name = 13
    size = []
    response = client.post(f"/api/v1/product-management/{name}/{size}", headers=headers)

    assert response.status_code == 409
    assert response.json == {'error': 'Invalid product name or size'}


def test_edit_product(client, jwt_token, db_session):

    headers = {'Authorization': f'Bearer {jwt_token}'}
    test_prod = {"product_name": "latte", "price": 4.75, "size": "M", "qty": 100 }

    prod = Products(**test_prod)
    db_session.add(prod)
    db_session.commit()

    edit_data = test_prod

    response = client.put("/api/v1/product-management/1", headers=headers, json=edit_data)

    assert response.status_code == 409 
    assert response.json['message'] == "no parameteres needed an update."

    ## invalid prod id

    response = client.put("/api/v1/product-management/2", headers=headers, json=edit_data)

    assert response.status_code == 409
    assert response.json['error'] == "invalid product id or nothing to update"

    ## check if editing prod #1 with params of #2 will fail
    test_prod = {"product_name": "latte", "price": 6.25, "size": "L", "qty": 100 }

    prod = Products(**test_prod)
    db_session.add(prod)
    db_session.commit()

    response = client.put("/api/v1/product-management/1", headers=headers, json=test_prod)

    assert response.status_code == 409 
    assert response.json['error'] == "error updating product name or size already exists!"

    ## verify updating name works 
    test_prod = {"product_name": "vanilla", "price": 6.25, "size": "L", "qty": 100 }

    response = client.put("/api/v1/product-management/1", headers=headers, json=test_prod)
    query_test_prod = Products.query.filter_by(id=1).first()

    assert response.status_code == 202
    assert response.json['message'] == "Updated product vanilla"
    assert query_test_prod.product_name == 'vanilla'


    ## verify updating size works 
    test_prod = {"product_name": "latte", "price": 6.25, "size": "XL", "qty": 100 }

    response = client.put("/api/v1/product-management/1", headers=headers, json=test_prod)
    query_test_prod = Products.query.filter_by(id=1).first()

    assert response.status_code == 202
    assert response.json['message'] == "Updated product latte"
    assert query_test_prod.size == 'XL'


    ## verify updating price works 
    test_prod = {"product_name": "latte", "price": 2.25, "size": "XL", "qty": 100 }

    response = client.put("/api/v1/product-management/1", headers=headers, json=test_prod)
    query_test_prod = Products.query.filter_by(id=1).first()

    assert response.status_code == 202
    assert response.json['message'] == "Updated product latte"
    assert query_test_prod.price == 2.25


    ## verify updating qty works 
    test_prod = {"product_name": "latte", "price": 4.75, "size": "M", "qty": 50 }

    response = client.put("/api/v1/product-management/1", headers=headers, json=test_prod)
    query_test_prod = Products.query.filter_by(id=1).first()

    assert response.status_code == 202
    assert response.json['message'] == "Updated product latte"
    assert query_test_prod.qty == 50


    ## verify error with invalid data
    test_prod = 76

    response = client.put("/api/v1/product-management/1", headers=headers, json=test_prod)
    query_test_prod = Products.query.filter_by(id=1).first()

    assert response.status_code == 400
    assert response.json['error'] == "invalid data"


def test_delete_product(client, jwt_token, db_session):

    headers = {'Authorization': f'Bearer {jwt_token}'}
    test_prod = {"product_name": "latte", "price": 4.75, "size": "M", "qty": 100 }

    prod = Products(**test_prod)
    db_session.add(prod)
    db_session.commit()

    response = client.delete("/api/v1/product-management/1", headers=headers)

    assert response.status_code == 202 
    assert response.json['message'] == '1: latte deleted from database.'

    # test invalid id or missing ID

    response = client.delete("/api/v1/product-management/1", headers=headers)

    assert response.status_code == 404
    assert response.json['error'] == "invalid product id or resource doesn't exist"

    # test missing auth header
    response = client.delete("/api/v1/product-management/1")

    assert response.status_code == 401
    assert response.json['msg'] == 'Missing Authorization Header'


