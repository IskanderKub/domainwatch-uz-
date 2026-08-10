# PostgreSQL connection setup: engine, session factory, and the declarative base
# that all SQLAlchemy models inherit from.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# engine manages the actual connection pool to Postgres
engine = create_engine(settings.postgres_url)

# SessionLocal is a factory for new Session objects, one per request/unit of work
# autocommit=False: nothing is written until we explicitly commit()
# autoflush=False: pending changes are not auto-flushed before every query
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all ORM models (Domain, CheckResult, ...) inherit from,
# so SQLAlchemy knows which tables/columns/relationships exist
Base = declarative_base()
