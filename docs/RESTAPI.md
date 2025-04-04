# Flask Backend

Flask backend supporting RESTAPI and mongodb.


## RESTAPI schema

### Users
Schema
```json
{
  "user_id": "user_001",
  "name": "Alice Johnson",
  "roles": "buyer",
  "email": "alice@example.com",
  "phone": "111-111-1111"
}
```

Endpoints

| Method | URL                | Description         |
|--------|--------------------|---------------------|
| GET    | `/users`           | Get all users       |
| GET    | `/users/<user_id>` | Get a user by ID    |
| POST   | `/users`           | Create a new user   |
| PUT    | `/users/<user_id>` | Update a user       |
| DELETE | `/users/<user_id>` | Delete a user       |

### Carts
```json
{
  "cart_id": "cart_00007",
  "user_id": "user_016",
  "items": [
    {
      "product_id": "prod_00003",
      "name": "Bluetooth Headphones",
      "quantity": 1,
      "price": 150.00
    }
  ]
}
```
Endpoints
| Method | URL                  | Description        |
|--------|-----------------------|--------------------|
| GET    | `/carts`             | Get all carts      |
| GET    | `/carts/<cart_id>`   | Get a cart by ID   |
| POST   | `/carts`             | Create a new cart  |
| PUT    | `/carts/<cart_id>`   | Update a cart      |
| DELETE | `/carts/<cart_id>`   | Delete a cart      |


### Products
Schema
```json
{
  "product_id": "prod_00014",
  "seller_id": "user_011",
  "name": "Backpack Organizer",
  "description": "Organize your backpack with multiple compartments.",
  "price": 22.50,
  "images": [
    "/sample_data/images/Backpack Organizer.jpg"
  ]
}
```
Endpoints
| Method | URL                      | Description           |
|--------|---------------------------|-----------------------|
| GET    | `/products`              | Get all products      |
| GET    | `/products/<product_id>` | Get a product by ID   |
| POST   | `/products`              | Create a new product  |
| PUT    | `/products/<product_id>` | Update a product      |
| DELETE | `/products/<product_id>` | Delete a product      |


### Orders
```json
{
  "order_id": "order_00001",
  "user_id": "user_003",
  "items": [
    {
      "product_id": "prod_00015",
      "name": "Wireless Earbuds",
      "quantity": 1,
      "unit_price": 100.00,
      "subtotal": 100.00
    },
    {
      "product_id": "prod_00019",
      "name": "Travel Pillow",
      "quantity": 1,
      "unit_price": 28.00,
      "subtotal": 28.00
    }
  ],
  "subtotal": 128.00,
  "tax": 12.80,
  "shipping_fee": 5.00,
  "total": 145.80,
  "payment_method": "credit_card",
  "payment_status": "completed",
  "transaction_date": "2025-03-28T15:00:00Z",
  "billing_address": {
    "name": "Alice Johnson",
    "street": "123 Maple St",
    "city": "Vancouver",
    "state": "BC",
    "zip": "V5K0A1",
    "country": "Canada"
  },
  "shipping_address": {
    "name": "Alice Johnson",
    "street": "123 Maple St",
    "city": "Vancouver",
    "state": "BC",
    "zip": "V5K0A1",
    "country": "Canada"
  },
  "submission_date": "2025-03-28T15:00:00Z"
}
```
Endpoints
| Method | URL                   | Description         |
|--------|------------------------|---------------------|
| GET    | `/orders`             | Get all orders      |
| GET    | `/orders/<order_id>`  | Get an order by ID  |
| POST   | `/orders`             | Create a new order  |
| PUT    | `/orders/<order_id>`  | Update an order     |
| DELETE | `/orders/<order_id>`  | Delete an order     |


### Permissions
Schema
```json
{
    "permissions": {
      "buyer": ["view_products", "make_purchase"],
      "seller": ["view_products", "list_product", "edit_product", "delete_product"],
      "admin": ["view_products", "edit_product", "delete_product", "delete_user", "manage_roles"]
    }
  }
```