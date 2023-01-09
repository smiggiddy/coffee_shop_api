from coffee_shop import create_app, db
from coffee_shop.models import Products, Orders, OrderItems
from flask_jwt_extended import create_access_token


def test_get_orders(client, jwt_token, db_session):
    # basic test to get all orders 
    headers = {'Authorization': f'Bearer {jwt_token}'}

    response = client.get("/api/v1/order-management", headers=headers)

    # testing empty order database
    assert response.status_code == 200
    assert response.json['data'] == []


def test_orders(client, jwt_token, db_session):

    headers = {'Authorization': f'Bearer {jwt_token}'}

    test_prod = {"product_name": "latte", "price": 4.75, "size": "M", "qty": 100 }

    prod = Products(**test_prod)
    db_session.add(prod)
    db_session.commit()

    # test new order 
    order_data = {
        'order_name': 'Deez Nutz', 
        'order_email': 'deez@nutz.big', 
        'items_list': [
            {'item_id': 1, 'qty': 30}
        ]
        }
    response = client.post("/api/v1/order-management", headers=headers, json=order_data)

    assert response.status_code == 201
    assert response.json['message'] == {'Deez Nutz': {'order_items': [{'item_id': 1, 'qty': 30}]}}

    # verify order items 
    order = Orders.query.filter_by(id=1).first()
    order_items = OrderItems.query.filter_by(id=1).first()

    assert order.order_total == 142.50
    assert order_items.item_id == 1
    assert order_items.qty == 30




