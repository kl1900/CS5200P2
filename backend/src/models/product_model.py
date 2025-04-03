from dataclasses import asdict, dataclass, field
from typing import List, Optional

from src.extensions import mongo
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
        return mongo.db.products.update_one(
            {"product_id": self.product_id}, {"$set": asdict(self)}, upsert=True
        )


def find_all_products() -> List[Product]:
    all_products = []
    for p in mongo.db.products.find():
        p = clean_mongo_doc(p)
        all_products.append(Product(**p))
    return all_products


def find_product_by_id(product_id) -> Optional[Product]:
    p = mongo.db.products.find_one({"product_id": product_id})
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
    
    result = mongo.db.products.insert_one(data)
    p = mongo.db.products.find_one({"_id": result.inserted_id})
    return Product(**clean_mongo_doc(p))


def update_product(product_id, data):
    # Get existing product
    product = find_product_by_id(product_id)
    if not product:
        return mongo.db.products.update_one({"product_id": "nonexistent"}, {"$set": {}})
    
    # Convert price to float if it's a string
    if "price" in data and isinstance(data["price"], str):
        data["price"] = float(data["price"])
    
    # Update only fields that are provided
    for k, v in data.items():
        if hasattr(product, k):
            setattr(product, k, v)
    
    return product.save()


def delete_product(product_id):
    return mongo.db.products.delete_one({"product_id": product_id})