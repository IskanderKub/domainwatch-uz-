# Aggregates all v1 routers under a single /api/v1 prefix.
from fastapi import APIRouter

from app.api.v1 import checks, domains, stats

router = APIRouter(prefix="/api/v1")
router.include_router(domains.router)
router.include_router(checks.router)
router.include_router(stats.router)
