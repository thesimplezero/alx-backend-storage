#!/usr/bin/env python3
"""
log_stats module
"""

from pymongo import MongoClient

def log_stats(mongo_collection):
    """
    Provides statistics about Nginx logs stored in MongoDB.
    """
    # Total logs
    total_logs = mongo_collection.count_documents({})
    print(f"Total logs: {total_logs}")

    # Method counts
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tMethod {method}: {count}")

    # Status check count
    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"Status check count: {status_check_count}")

    # Top 10 IPs
    top_ips_pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = list(mongo_collection.aggregate(top_ips_pipeline))
    print("Top 10 IPs:")
    for ip_info in top_ips:
        print(f"\t{ip_info['_id']}: {ip_info['count']}")

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    log_stats(logs_collection)
