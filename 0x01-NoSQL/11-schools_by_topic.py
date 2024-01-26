#!/usr/bin/env python3
"""
schools_by_topic module
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns a list of schools that have a specific topic.

    Args:
        mongo_collection: MongoDB collection object.
        topic: The topic to search for.

    Returns:
        List of schools matching the specified topic.
    """
    filter_query = {"topics": {"$in": [topic]}}
    schools = list(mongo_collection.find(filter_query))
    return schools
