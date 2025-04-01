from dataclasses import asdict, dataclass, field
from typing import List

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
            {"product_id": self.product_id}, {"$set": asdict(self)}
        )


def find_all_products() -> List[Product]:
    all_products = []
    for p in mongo.db.products.find():
        p = clean_mongo_doc(p)
        all_products.append(Product(**p))
    return all_products


def find_product_by_id(product_id) -> Product:
    p = mongo.db.products.find_one({"product_id": product_id})
    return Product(**clean_mongo_doc(p))


def create_product(data) -> Product:
    result = mongo.db.products.insert_one(data)
    p = mongo.db.products.find_one({"_id": result.inserted_id})
    return Product(**clean_mongo_doc(p))


def update_product(product_id, data):
    product = find_product_by_id(product_id)
    for k, v in data:
        setattr(product, k, v)
    return product.save()


def delete_product(product_id):
    return mongo.db.products.delete_one({"product_id": product_id})
