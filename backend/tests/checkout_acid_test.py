import threading
from unittest.mock import patch, MagicMock

def test_checkout_creates_complete_order(client, db):
    user_id = "user_001"
    cart_id = "cart_00089"

    db.cart.insert_one({
        "cart_id": cart_id,
        "user_id": user_id,
        "status": "active",
        "items": [
            {
                "product_id": "prod_00015",
                "name": "Wireless Earbuds",
                "quantity": 1,
                "price": 100.00
            }
        ]
    })

    response = client.post("/api/checkout", json={
        "user_id": user_id,
        "cart_id": cart_id,
        "payment_method": "credit_card",
        "billing_address": {
            "name": "Foo bar",
            "street": "example Lane",
            "city": "Vancouver",
            "state": "BC",
            "zip": "",
            "country": "Canada"
        },
        "shipping_address": {
            "name": "Foo Bar",
            "street": "example Lane",
            "city": "Vancouver",
            "state": "BC",
            "zip": "",
            "country": "Canada"
        }
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "Checkout successful"

    # Validate order
    order = db.orders.find_one({"user_id": user_id})
    assert order is not None

    assert "order_id" in order
    assert order["payment_method"] == "credit_card"
    assert order["payment_status"] == "completed"

    # Financials
    assert order["subtotal"] == 100.00
    assert order["tax"] == 10.00
    assert order["shipping_fee"] == 5.00
    assert order["total"] == 115.00

    # Items
    assert len(order["items"]) == 1
    item = order["items"][0]
    assert item["product_id"] == "prod_00015"
    assert item["unit_price"] == 100.00
    assert item["subtotal"] == 100.00

    # Addresses
    assert order["billing_address"]["city"] == "Vancouver"
    assert order["shipping_address"]["country"] == "Canada"

    # Timestamps
    for field in ["transaction_date", "submission_date"]:
        assert field in order
        assert order[field].endswith("Z")  # UTC format

    # Cart should be checked_out
    cart = db.cart.find_one({"cart_id": cart_id})
    assert cart["status"] == "checked_out"

    # New active cart exists
    new_cart = db.cart.find_one({"user_id": user_id, "status": "active"})
    assert new_cart is not None
    assert new_cart["items"] == []


def test_checkout_race_condition(client, db):
    user_id = "user_race"
    cart_id = "cart_race"

    # Insert a shared cart for both threads
    db.cart.insert_one({
        "cart_id": cart_id,
        "user_id": user_id,
        "status": "active",
        "items": [
            {
                "product_id": "prod_00015",
                "name": "Wireless Earbuds",
                "quantity": 1,
                "price": 100.00
            }
        ]
    })

    checkout_payload = {
        "user_id": user_id,
        "cart_id": cart_id,
        "payment_method": "credit_card",
        "billing_address": {
            "name": "Foo bar",
            "street": "example Lane",
            "city": "Vancouver",
            "state": "BC",
            "zip": "",
            "country": "Canada"
        },
        "shipping_address": {
            "name": "Foo Bar",
            "street": "example Lane",
            "city": "Vancouver",
            "state": "BC",
            "zip": "",
            "country": "Canada"
        }
    }

    results = [None, None]

    def run_checkout(index):
        results[index] = client.post("/api/checkout", json=checkout_payload)

    # Simulate concurrent checkouts
    threads = [
        threading.Thread(target=run_checkout, args=(0,)),
        threading.Thread(target=run_checkout, args=(1,))
    ]
    for t in threads: t.start()
    for t in threads: t.join()

    # One should succeed, one should fail
    status_codes = [r.status_code for r in results]
    assert sorted(status_codes) == [200, 400]

    # Only one order should exist
    orders = list(db.orders.find({"user_id": user_id}))
    assert len(orders) == 1

    order = orders[0]

    # Verify order structure
    assert order["order_id"].startswith("order_")
    assert order["payment_method"] == "credit_card"
    assert order["payment_status"] == "completed"
    assert order["subtotal"] == 100.00
    assert order["tax"] == 10.00
    assert order["shipping_fee"] == 5.00
    assert order["total"] == 115.00
    assert order["billing_address"]["city"] == "Vancouver"
    assert order["shipping_address"]["country"] == "Canada"
    assert order["transaction_date"].endswith("Z")
    assert order["submission_date"].endswith("Z")

    # Ensure cart is marked checked_out
    cart = db.cart.find_one({"cart_id": cart_id})
    assert cart["status"] == "checked_out"

    # New active cart should exist
    new_cart = db.cart.find_one({"user_id": user_id, "status": "active"})
    assert new_cart is not None
    assert new_cart["items"] == []
    
def test_checkout_rolls_back_when_update_cart_fails(client, db):
    user_id = "user_patch"
    cart_id = "cart_patch"

    # Insert test cart
    db.cart.insert_one({
        "cart_id": cart_id,
        "user_id": user_id,
        "status": "active",
        "items": [
            {"product_id": "prod_001", "name": "Item", "quantity": 1, "price": 99.99}
        ]
    })


    with patch("src.routes.checkout_routes.txn_ops_factory", side_effect=Exception("simulated update failure")):
        response = client.post("/api/checkout", json={
            "user_id": "user_x",
            "cart_id": "cart_x",
            "payment_method": "credit_card",
            "billing_address": {},
            "shipping_address": {}
        })

    assert response.status_code == 400
    assert "simulated update failure" in response.get_json()["error"].lower()

    # Nothing should be committed
    assert db.orders.count_documents({"user_id": user_id}) == 0
    assert db.cart.find_one({"cart_id": cart_id})["status"] == "active"
    assert db.cart.count_documents({"user_id": user_id, "status": "active"}) == 1
    