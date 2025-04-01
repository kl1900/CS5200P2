"Utility functions"

def serialize_id(document):
    document["_id"] = str(document["_id"])
    return document
