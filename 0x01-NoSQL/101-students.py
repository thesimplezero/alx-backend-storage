#!/usr/bin/env python3
"""
students module
"""

from pymongo import MongoClient

def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    """
    pipeline = [
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "topics": 1,
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]

    top_students = list(mongo_collection.aggregate(pipeline))
    return top_students

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students
    top_students_data = top_students(students_collection)
