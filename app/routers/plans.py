

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.dependencies import DbSession, CurrentUser, require_role
from app.models import Plan, Membership
from app.schemas import PlanCreate, PlanResponse

router = APIRouter()


@router.get("/", response_model=list[PlanResponse])
def list_plans(db: DbSession):
    return db.scalars(select(Plan).order_by(Plan.id)).all()


@router.post("/", response_model=PlanResponse, status_code=201)
def create_plan(
    data: PlanCreate,
    db: DbSession,
    admin=__import__("fastapi").Depends(require_role("admin")),
):
    plan = Plan(**data.model_dump())
    db.add(plan)

    try:
        db.commit()
        db.refresh(plan)
    except Exception:
        db.rollback()
        raise

    return plan


@router.put("/{plan_id}", response_model=PlanResponse)
def update_plan(
    plan_id: int,
    data: PlanCreate,
    db: DbSession,
    admin=__import__("fastapi").Depends(require_role("admin")),
):
    plan = db.get(Plan, plan_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    for key, value in data.model_dump().items():
        setattr(plan, key, value)

    db.commit()
    db.refresh(plan)

    return plan


@router.delete("/{plan_id}", status_code=204)
def delete_plan(
    plan_id: int,
    db: DbSession,
    admin=__import__("fastapi").Depends(require_role("admin")),
):
    plan = db.get(Plan, plan_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    used = db.scalar(
        select(Membership.id).where(Membership.plan_id == plan_id).limit(1)
    )

    if used:
        raise HTTPException(
            status_code=409,
            detail="Plan has membership history and cannot be deleted",
        )

    db.delete(plan)
    db.commit()
