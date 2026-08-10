# REST endpoint for per-domain aggregated statistics.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.domain import DomainStats
from app.services.domain_service import DomainService
from app.services.stats_service import StatsService

router = APIRouter(prefix="/domains/{domain_id}/stats", tags=["stats"])


@router.get("", response_model=DomainStats)
def get_domain_stats(domain_id: int, db: Session = Depends(get_db)):
    domain = DomainService(db).get_domain(domain_id)
    if domain is None:
        raise HTTPException(status_code=404, detail="Domain not found")
    return StatsService(db).get_domain_stats(domain_id)
