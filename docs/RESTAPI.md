# Flask Backend

Flask backend supporting RESTAPI and mongodb.


## Folder Structure

```
flask-backend/
├── app.py                    # Entry point to start the Flask app
├── requirements.txt          # Python dependencies
│
└── src/
    ├── __init__.py           # Application factory (create_app)
    ├── extensions.py         # Shared extensions (e.g., PyMongo)
    │
    ├── models/               # MongoDB access layer and logic
    │   ├── user_model.py
    │   ├── cart_model.py
    │   ├── product_model.py
    │   └── order_model.py
    │
    ├── routes/               # API routes (Flask blueprints)
    │   ├── user_routes.py
    │   ├── cart_routes.py
    │   ├── product_routes.py
    │   └── order_routes.py
    │
    └── utils.py               # Helpers and decorators

```

## How it works
- app.py: Starts the Flask server using the app factory from src/__init__.py.
- routes/: Contains modular blueprints for each API section (users, products, etc.).
- models/: Encapsulates all MongoDB operations per resource.
- utils.py: Utility functions like serializers and decorators.
