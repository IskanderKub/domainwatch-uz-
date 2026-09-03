# MongoDB connection setup, used for storing raw page-text snapshots.
from pymongo import MongoClient

from app.core.config import settings

# MongoClient connects lazily - no actual network call happens until we query/insert
mongo_client = MongoClient(settings.mongo_url, serverSelectionTimeoutMS=3000, tz_aware=True)
mongo_db = mongo_client[settings.mongo_db_name]

# Collection holding one document per (domain, check) with the extracted page text
snapshots_collection = mongo_db["snapshots"]


def ensure_indexes():
    snapshots_collection.create_index([("domain_id", 1), ("checked_at", -1)])
