import threading

import pytest


@pytest.fixture(autouse=True)
def clean_db(db):
    yield
    for name in db.list_collection_names():
        db.drop_collection(name)


def test_checkout_succeeds(client, db):
    user_id = "user_abc"
    cart_id = "cart_xyz"

    # No inventory setup needed (infinite stock model)

    db.cart.insert_one(
        {
            "cart_id": cart_id,
            "user_id": user_id,
            "status": "active",
            "items": [
                {
                    "product_id": "prod_001",
                    "name": "Earpods",
                    "quantity": 2,
                    "price": 99.99,
                }
            ],
        }
    )

    response = client.post(
        "/api/checkout", json={"user_id": user_id, "cart_id": cart_id}
    )

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


def test_checkout_race_condition(client, db):
    user_id = "user_race"
    cart_id = "cart_race"

    # Seed the shared cart
    db.cart.insert_one(
        {
            "cart_id": cart_id,
            "user_id": user_id,
            "status": "active",
            "items": [
                {
                    "product_id": "prod_race",
                    "name": "Gaming Mouse",
                    "quantity": 1,
                    "price": 79.99,
                }
            ],
        }
    )

    results = [None, None]

    def attempt_checkout(index):
        res = client.post(
            "/api/checkout", json={"user_id": user_id, "cart_id": cart_id}
        )
        results[index] = res

    # Run 2 checkout requests "simultaneously"
    threads = [
        threading.Thread(target=attempt_checkout, args=(0,)),
        threading.Thread(target=attempt_checkout, args=(1,)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # One should succeed (200), one should fail (400)
    statuses = [r.status_code for r in results]
    assert sorted(statuses) == [200, 400]

    # Only one order should exist
    assert db.orders.count_documents({"user_id": user_id}) == 1

    # The original cart should be marked as checked_out
    cart = db.cart.find_one({"cart_id": cart_id})
    assert cart["status"] == "checked_out"

    # A new active cart should exist
    assert db.cart.count_documents({"user_id": user_id, "status": "active"}) == 1
