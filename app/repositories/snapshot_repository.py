# Data-access layer for page-text snapshots stored in MongoDB.
# Kept separate from PostgreSQL repositories since it uses a different driver (pymongo).
from datetime import datetime, timezone

from pymongo.collection import Collection

from app.core.mongo import snapshots_collection

from bson import ObjectId


class SnapshotRepository:
    def __init__(self, collection: Collection = snapshots_collection):
        self.collection = collection

    def save(self, domain_id: int, text_content: str) -> ObjectId:
        result = self.collection.insert_one(
            {
                "domain_id": domain_id,
                "checked_at": datetime.now(timezone.utc),
                "text_content": text_content,
            }
        )
        return result.inserted_id

    def attach_check_id(self, snapshot_id: ObjectId, check_id: int) -> None:
        self.collection.update_one(
            {"_id": snapshot_id},
            {"$set": {"check_id":check_id}},
        )

    def get_latest(self, domain_id: int) -> dict | None:
        # sort by checked_at descending and take the first document
        return self.collection.find_one(
            {"domain_id": domain_id}, sort=[("checked_at", -1)]
        )
