from dataclasses import asdict, dataclass, field
from typing import List, Optional

from src.db import get_db
from src.utils import clean_mongo_doc


@dataclass
class Product:
    product_id: str
    seller_id: str
    name: str
    description: str
    price: float
    images: List = field(default_factory=list)
    
    def save(self):
        "save current data into database"
        return get_db().products.update_one(
            {"product_id": self.product_id}, {"$set": asdict(self)}, upsert=True
        )


def find_all_products(current_user=None) -> List[Product]:
    all_products = []
    # Default: return all products unless filtering is needed
    query = {}

    if current_user:
        role = current_user.get("roles")
        user_id = current_user.get("user_id")

        if role == "seller":
            # Only return products listed by the seller
            query["seller_id"] = user_id

        # Maybe for the buyer here too if later needed

    for p in get_db().products.find(query):
        p = clean_mongo_doc(p)
        all_products.append(Product(**p))
    return all_products


def find_product_by_id(product_id) -> Optional[Product]:
    p = get_db().products.find_one({"product_id": product_id})
    if not p:
        return None
    return Product(**clean_mongo_doc(p))


def create_product(data) -> Product:
    # Ensure data has required fields
    required_fields = ["product_id", "seller_id", "name", "description", "price"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    # Convert price to float if it's not already
    if isinstance(data["price"], str):
        data["price"] = float(data["price"])
    
    # Ensure images is a list
    if "images" not in data:
        data["images"] = []
    
    result = get_db().products.insert_one(data)
    p = get_db().products.find_one({"_id": result.inserted_id})
    return Product(**clean_mongo_doc(p))


def update_product(product_id, data):
    # Get existing product
    product = find_product_by_id(product_id)
    if not product:
        return get_db().products.update_one({"product_id": "nonexistent"}, {"$set": {}})
    
    # Convert price to float if it's a string
    if "price" in data and isinstance(data["price"], str):
        data["price"] = float(data["price"])
    
    # Update only fields that are provided
    for k, v in data.items():
        if hasattr(product, k):
            setattr(product, k, v)
    
    return product.save()


def delete_product(product_id):
    return get_db().products.delete_one({"product_id": product_id})