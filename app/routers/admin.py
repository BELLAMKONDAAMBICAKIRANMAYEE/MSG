
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.dependencies import DbSession, require_role
from app.models import Membership, User
from app.schemas import TrainerAssignment, MembershipResponse,UserResponse

router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    db: DbSession,
    admin=Depends(require_role("admin")),
):
    users = db.scalars(
        select(User).order_by(User.id)
    ).all()

    return users

@router.patch(
    "/memberships/{membership_id}/assign",
    response_model=MembershipResponse,
)
def assign_trainer(
    membership_id: int,
    data: TrainerAssignment,
    db: DbSession,
    admin=Depends(require_role("admin")),
):
    membership = db.get(Membership, membership_id)

    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")

    trainer = db.scalar(
        select(User).where(
            User.id == data.trainer_id,
            User.role == "trainer",
            User.is_active.is_(True),
        )
    )

    if not trainer:
        raise HTTPException(status_code=404, detail="Active trainer not found")

    membership.trainer_id = trainer.id

    db.commit()
    db.refresh(membership)

    return membership
