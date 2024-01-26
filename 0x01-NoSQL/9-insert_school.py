#!/usr/bin/env python3
"""
insert_school module
"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document into the collection based on keyword arguments."""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
