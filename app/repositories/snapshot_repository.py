# Data-access layer for page-text snapshots stored in MongoDB.
# Kept separate from PostgreSQL repositories since it uses a different driver (pymongo).
from datetime import datetime, timezone

from pymongo.collection import Collection

from app.core.mongo import snapshots_collection


class SnapshotRepository:
    def __init__(self, collection: Collection = snapshots_collection):
        self.collection = collection

    def save(self, domain_id: int, text_content: str) -> None:
        self.collection.insert_one(
            {
                "domain_id": domain_id,
                "checked_at": datetime.now(timezone.utc),
                "text_content": text_content,
            }
        )

    def get_latest(self, domain_id: int) -> dict | None:
        # sort by checked_at descending and take the first document
        return self.collection.find_one(
            {"domain_id": domain_id}, sort=[("checked_at", -1)]
        )
