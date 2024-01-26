#!/usr/bin/env python3
"""
update_topics module
"""

def update_topics(mongo_collection, name, topics):
    """Changes all topics of school document based on name."""
    filter_query = {"name": name}
    update_query = {"$set": {"topics": topics}}
    result = mongo_collection.update_many(filter_query, update_query)
    return result.modified_count
