# FastAPI application entrypoint.
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1 import router as api_v1_router
from app.core.postgres import Base, engine
from app.core.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create_all is idempotent (no-op for tables that already exist) - fine for a
    # pet project; a production service would use Alembic migrations instead
    Base.metadata.create_all(bind=engine)
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(title="DomainWatch.uz", lifespan=lifespan)
app.include_router(api_v1_router)


@app.get("/health")
def health():
    return {"status": "ok"}
