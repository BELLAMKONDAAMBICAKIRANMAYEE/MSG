from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import (
    auth,
    plans,
    memberships,
    attendance,
    admin,
    trainer,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Development only; use Alembic migrations in production.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Gym Management System API",
    version="1.0.0",
    description="Manage gym members, plans, trainers and attendance",
    lifespan=lifespan,
)


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(plans.router, prefix="/plans", tags=["Plans"])

app.include_router(
    memberships.router,
    prefix="/memberships",
    tags=["Memberships"],
)

app.include_router(
    attendance.router,
    prefix="/attendance",
    tags=["Attendance"],
)

app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(trainer.router, prefix="/trainer", tags=["Trainer"])




@app.get("/")
def home():
    return {
        "message": "Gym Management System API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}