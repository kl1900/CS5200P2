"Utility functions"

from functools import wraps


def clean_mongo_doc(doc):
    "remove '_id' from mongo data"
    doc = doc.copy()
    doc.pop("_id", None)
    return doc


def clean_mongo_result(func):
    """
    Decorator to remove '_id' from MongoDB documents
    returned by a function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        # Handle single document
        if isinstance(result, dict):
            result = result.copy()
            result.pop("_id", None)
            return result

        # Handle list of documents
        if isinstance(result, list):
            return [{k: v for k, v in doc.items() if k != "_id"} for doc in result]

        return result  # fallback

    return wrapper
