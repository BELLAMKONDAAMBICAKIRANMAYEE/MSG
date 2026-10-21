
from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.dependencies import DbSession, require_role
from app.models import Membership, User
from app.schemas import UserResponse
from app.services import expire_memberships

router = APIRouter()


@router.get("/members", response_model=list[UserResponse])
def assigned_members(
    db: DbSession,
    trainer=Depends(require_role("trainer")),
):
    expire_memberships(db)

    members = db.scalars(
        select(User)
        .join(Membership, Membership.member_id == User.id)
        .where(
            Membership.trainer_id == trainer.id,
            Membership.is_active.is_(True),
        )
        .distinct()
        .order_by(User.name)
    ).all()

    return members
