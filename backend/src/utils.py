"Utility functions"


def serialize_id(document):
    document["_id"] = str(document["_id"])
    return document


def clean_mongo_doc(doc):
    "remove '_id' from mongo data"
    doc = doc.copy()
    doc.pop("_id", None)
    return doc
