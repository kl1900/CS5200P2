# CS5200P2

## Setting up application

Having docker Installed.

After git pulled this repo or unzipped this repo, open terminal

```
cd <project repo folder>
```

Run

```
docker-compose up --build -d
```

It runs 4 services:

1. mongo
2. mongo-express (mongodb admin) url: http://localhost:8081
   - usrname `admin`
   - password `5200`
3. flask server url: http://localhost:8000
4. react front end url: http://localhost:5173

to insert data, run

```
docker exec -it flask-backend python3 import_data.py
```

to cleanup containers

```
docker-compose down --volumes --remove-orphans
```

## Topic and features:

Secure Online Marketplace (E-Commerce):

- Users can buy/sell products, add to cart, and checkout.
- Transactions should be ACID-compliant (ensure inventory updates correctly).
- RBAC: Buyers, sellers, and admins with different permissions.
- Reviews & Recommendations using MongoDB aggregation.



## How to Explore different features:

Please visit http://localhost:5173/ for frontend page. There is a role-based authentication process needed to explore the CRUD operation. User can be defined as "buyer", "seller", and "admin" based on their email address. 

For example, 

emma@example.com is an admin, which has all the permission to edit, add, delete, update products.  There will be more features available exclusively to admin later.

alice@example.com is a buyer, which can not be doing any CRUD operation in our current page.

bob@fakeemail.com is a seller, which can only add, edit, update and delete product. (No more permission in later development)

In order to explore any of the CRUD features, click on login to authenticate an user first. And then, enter email address above to finish the login process (admin recommended). Once login, you would able to perform the CRUD operation in Products page. 

Notice that buyer can not do anything as there are no permission granted to buyer.

## Authentication Testing

Use POSTMAN or other API platform

<u>Step 1: Login to Get a JWT</u>

```bash
POST http://localhost:5000/auth/login
```

**Body** → Choose `raw` → JSON:

```json
{
  "email": "emma@example.com"
}
```

This user must have a `"roles"` field like `"admin"`, `"seller"`, or `"buyer"` (which in our database, there must be a role)

<u>Step 2: Copy the Token</u>

In Postman, save the token or use **"Environment Variables"** to store it (optional).

<u>Step 3: Use Token to Call a Protected Route</u>

For **each protected route**, include this in the request header:

```makefile
Authorization: Bearer <paste-your-token-here>
```

<u>Step 4: Admin Test — GET Users (Admin Only)</u>

```bash
GET http://localhost:5000/users/
```

**Header**:

```sql

Authorization: Bearer <admin-token>
```

Expected:

**200 with list of users**

403 if not admin

Testing other routes if needed

## MS1:

### Task 1: MongoDB Schema Design and Data Population(10 pts, ~3 hrs)

- [x] Define a document-based schema for the chosen application.
- [x] Minimum of 5 distinct collections with clear relationships.
- [x] At least 20 sample documents per collection that store main data/ transactions/relationships (not including collections used for type/categorization).
- [x] Store nested JSON data where applicable.

Deliverables:

1. Implementation codes:

   - [x] (Kuo) MongoDB database setup
   - [x] (Xu) sample data population

2. Documentation:
   1. [x] (Weifan) page description of the project
   2. [x] (Raagini) Schema showing collections and relationships using example JSON documents for each collection

### Task 2: CRUD Operations & API Development (20 pts, ~5 hrs)

- (Kuo) Implement a REST API (Node.js, Express, or Flask) to interact with MongoDB.
- Support full Create, Read, Update, Delete (CRUD) operations for at least 1 collection (simple front end).
  - (Raagini) product (seller user) front end
  - (Xu) product back end
- (Weifan) Implement secure authentication (JWT or Firebase Auth).

Deliverables:
Implementation codes: - API source code with implementation of CRUD operations
Documentation: - [x] README with setup instruction for the chosen framework and tools. - API documentation with endpoints, request/response examples, and CRUD operations. - (Kuo) [RESTAPI for backend](docs/BackendAPI.md) - (Raagini) [CRUD for product](docs/CRUD_operations.md)
