# Online Retail API Documentation

This API provides endpoints to manage products in the online retail application. The API is designed as a RESTful service that supports the standard Create, Read, Update, and Delete (CRUD) operations.

> **Note:** The API is assumed to be hosted on `http://localhost:8000`. Adjust the base URL as needed for your production environment.

---

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [Products Endpoints](#products-endpoints)
  - [GET /products](#get-products)
  - [GET /products/:id](#get-productsid)
  - [POST /products](#post-products)
  - [PUT /products/:id](#put-productsid)
  - [DELETE /products/:id](#delete-productsid)
- [CRUD Examples](#crud-examples)
- [Error Handling](#error-handling)
- [Future Work: Cart Endpoints](#future-work-cart-endpoints)

---

## Setup Instructions

1. **Backend Setup:**
   - Ensure you have a backend server running on port `8000` (or update the API base URL in your frontend).
   - Implement a RESTful API that supports CRUD operations for products.
   - Use your preferred backend language or framework (e.g., Node.js with Express, Python with Flask/Django, etc.).

2. **Frontend Setup:**
   - Install the required dependencies by running:
     ```bash
     npm install
     ```
   - Start the development server:
     ```bash
     npm run dev
     ```
   - The frontend application (React) will be accessible on the URL provided by your development server (commonly `http://localhost:3000`).

3. **Configuration:**
   - The frontend fetches products from `http://localhost:8000/products/`. Update this URL if your backend is hosted elsewhere.
   - Ensure that CORS is configured on your backend server to allow requests from your frontend's origin.

---

## Products Endpoints

### GET /products

**Description:**  
Retrieve a list of all available products.

**Request:**

- **Method:** GET  
- **URL:** `http://localhost:8000/products/`

**Response Example (200 OK):**

```json
[
  {
    "product_id": "prod_001",
    "name": "Wireless Mouse",
    "price": 25.99,
    "description": "A reliable wireless mouse with ergonomic design.",
    "seller_id": "user_002"
  },
  {
    "product_id": "prod_002",
    "name": "Mechanical Keyboard",
    "price": 89.99,
    "description": "A durable keyboard with customizable backlighting.",
    "seller_id": "user_002"
  }
]
```

### GET /products/:id

**Description:**  
Retrieve details of a single product by its product_id.

**Request:**

- **Method:** GET
- **URL:** `http://localhost:8000/products/{product_id}`

**Response Example (200 OK):**

```json
{
  "product_id": "prod_001",
  "name": "Wireless Mouse",
  "price": 25.99,
  "description": "A reliable wireless mouse with ergonomic design.",
  "seller_id": "user_002"
}
```

**Error Example (404 Not Found):**

```json
{
  "error": "Product not found"
}
```

### POST /products

**Description:**  
Create a new product entry.

**Request:**

- **Method:** POST
- **URL:** `http://localhost:8000/products/`
- **Headers:**
  - Content-Type: application/json

**Request Body Example:**

```json
{
  "product_id": "prod_003",
  "name": "USB-C Hub",
  "price": 49.99,
  "description": "Multi-port USB-C hub with HDMI and Ethernet.",
  "seller_id": "user_002"
}
```

**Response Example (201 Created):**

```json
{
  "message": "Product created successfully",
  "product": {
    "product_id": "prod_003",
    "name": "USB-C Hub",
    "price": 49.99,
    "description": "Multi-port USB-C hub with HDMI and Ethernet.",
    "seller_id": "user_002"
  }
}
```

**Error Example (400 Bad Request):**

```json
{
  "error": "Invalid input data"
}
```

### PUT /products/:id

**Description:**  
Update an existing product. The endpoint uses the product's product_id as the identifier.

**Request:**

- **Method:** PUT
- **URL:** `http://localhost:8000/products/{product_id}`
- **Headers:**
  - Content-Type: application/json

**Request Body Example:**

```json
{
  "name": "Wireless Mouse - Updated",
  "price": 27.99,
  "description": "Updated description: Ergonomic design with improved battery life.",
  "seller_id": "user_002"
}
```

**Response Example (200 OK):**

```json
{
  "message": "Product updated successfully",
  "product": {
    "product_id": "prod_001",
    "name": "Wireless Mouse - Updated",
    "price": 27.99,
    "description": "Updated description: Ergonomic design with improved battery life.",
    "seller_id": "user_002"
  }
}
```

**Error Example (404 Not Found):**

```json
{
  "error": "Product not found"
}
```

### DELETE /products/:id

**Description:**  
Delete a product using its product_id.

**Request:**

- **Method:** DELETE
- **URL:** `http://localhost:8000/products/{product_id}`

**Response Example (200 OK):**

```json
{
  "message": "Product deleted successfully"
}
```

**Error Example (404 Not Found):**

```json
{
  "error": "Product not found"
}
```

## CRUD Examples

Below are example commands using curl to perform CRUD operations against the API.

### Create a Product (POST)

```bash
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "prod_004",
    "name": "Bluetooth Speaker",
    "price": 59.99,
    "description": "Portable Bluetooth speaker with deep bass.",
    "seller_id": "user_002"
  }'
```

### Read All Products (GET)

```bash
curl http://localhost:8000/products/
```

### Update a Product (PUT)

```bash
curl -X PUT http://localhost:8000/products/prod_004 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bluetooth Speaker - Updated",
    "price": 64.99,
    "description": "Updated description: Enhanced sound quality with longer battery life.",
    "seller_id": "user_002"
  }'
```

### Delete a Product (DELETE)

```bash
curl -X DELETE http://localhost:8000/products/prod_004
```

## Error Handling

All endpoints are expected to return proper HTTP status codes and JSON error messages. Common error status codes include:

- **400 Bad Request**: The request data is invalid or missing required fields.

- **404 Not Found**: The requested product does not exist.

- **500 Internal Server Error**: An unexpected error occurred on the server.

Example of an error response:

```json
{
  "error": "Detailed error message"
}
```

## Future Work: Cart Endpoints

The CartPage currently displays a placeholder message ("Cart Management Coming Soon 🛒"). In the future, similar CRUD endpoints can be developed for cart operations (e.g., adding items to a cart, removing items, and updating quantities).