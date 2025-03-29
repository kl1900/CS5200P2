# CS5200P2

Topic and features:
Secure Online Marketplace (E-Commerce):
- Users can buy/sell products, add to cart, and checkout.
- Transactions should be ACID-compliant (ensure inventory updates correctly).
- RBAC: Buyers, sellers, and admins with different permissions.
- Reviews & Recommendations using MongoDB aggregation.

## MS1:
### Task 1: MongoDB Schema Design and Data Population(10 pts, ~3 hrs)
- Define a document-based schema for the chosen application.
- Minimum of 5 distinct collections with clear relationships.
- At least 20 sample documents per collection that store main data/ transactions/relationships (not including collections used for type/categorization).
- Store nested JSON data where applicable.

Deliverables:
1. Implementation codes: 
    - (Kuo) MongoDB database setup
    - (Xu) sample data population

2. Documentation:
    1. (Weifan) page description of the project
    2. (Raagini) Schema showing collections and relationships using example JSON documents for each collection


DOC location: https://docs.google.com/document/d/1exYK52GJdgID_IRjyN4bXN-ooOoBZFrecLefyAYfRbg/edit?usp=sharing

### Task 2: CRUD Operations & API Development (20 pts, ~5 hrs) 
- Implement a REST API (Node.js, Express, or Flask) to interact with MongoDB.
- Support full Create, Read, Update, Delete (CRUD) operations for at least 1 collection.
- Implement secure authentication (JWT or Firebase Auth).

Deliverables:
Implementation codes: 
    - API source code with implementation of CRUD operations
Documentation:
    - README with setup instruction for the chosen framework and tools.
    - API documentation with endpoints, request/response examples, and CRUD operations.
