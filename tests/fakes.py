from datetime import datetime, timezone


class FakeSnapshotRepository:
    def __init__(self):
        self.documents = []

    def save(self, domain_id: int, text_content: str):
        _id = len(self.documents)
        self.documents.append(
            {
                "domain_id": domain_id,
                "checked_at": datetime.now(timezone.utc),
                "text_content": text_content,
                "_id": _id,
            }
        )
        return _id

    def get_latest(self, domain_id: int) -> dict | None:
        matching = []
        for doc in self.documents:
            if doc["domain_id"] == domain_id:
                matching.append(doc)

        if not matching:
            return None
        return max(matching, key=lambda doc: doc["checked_at"])

    def attach_check_id(self, snapshot_id: int, check_id: int) -> None:
        for doc in self.documents:
            if doc["_id"] == snapshot_id:
                doc["check_id"] = check_id
                break
