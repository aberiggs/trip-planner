"""Module providing functino to create collection"""


def create_collection(db, collection_name):
    """Function that creates a collection but ignore if collection aleady exists"""
    try:
        db.create_collection(collection_name)
    except Exception:
        pass
