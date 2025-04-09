# tests/test_checkout_infinite_stock.py

import pytest

@pytest.fixture(autouse=True)
def clean_db(db):
    yield
    import pdb
    pdb.set_trace()
    for name in db.list_collection_names():
        db.drop_collection(name)

def test_checkout_succeeds(client, db):
    user_id = "user_abc"
    cart_id = "cart_xyz"

    # No inventory setup needed (infinite stock model)

    db.cart.insert_one({
        "cart_id": cart_id,
        "user_id": user_id,
        "status": "active",
        "items": [
            {"product_id": "prod_001", "name": "Earpods", "quantity": 2, "price": 99.99}
        ]
    })

    response = client.post("/api/checkout", json={
        "user_id": user_id,
        "cart_id": cart_id
    })

    assert response.status_code == 200
    assert response.get_json()["message"] == "Checkout successful"

    # Order created
    assert db.orders.count_documents({"user_id": user_id}) == 1
    order = db.orders.find_one({"user_id": user_id})
    assert order["items"][0]["product_id"] == "prod_001"

    # Old cart marked as checked_out
    assert db.cart.find_one({"cart_id": cart_id})["status"] == "checked_out"

    # New cart created with status active
    new_cart = db.cart.find_one({"user_id": user_id, "status": "active"})
    assert new_cart is not None
    assert new_cart["items"] == []
