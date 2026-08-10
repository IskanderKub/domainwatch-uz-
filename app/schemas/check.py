# Pydantic schemas for check-result and snapshot API responses.
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CheckResultRead(BaseModel):
    """A single check result as returned by the API."""

    id: int
    domain_id: int
    checked_at: datetime
    is_available: bool
    status_code: int | None
    response_time_ms: float | None
    similarity_ratio: float | None
    is_suspected_defacement: bool
    error_message: str | None

    model_config = ConfigDict(from_attributes=True)


class SnapshotRead(BaseModel):
    """A raw page-text snapshot, as stored in MongoDB."""

    domain_id: int
    checked_at: datetime
    text_content: str
