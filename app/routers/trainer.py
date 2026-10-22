
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy import select

from app.dependencies import DbSession, require_role
from app.models import Membership, User,Attendance
from app.schemas import UserResponse,TrainerAssignment,MembershipResponse

from app.services import (
    subscribe_member,
    expire_memberships,
    renew_membership,
)

router = APIRouter()




# Get the logged-in trainer's details
@router.get("/")
def get_trainer(
    db: DbSession,
    trainer=Depends(require_role("trainer")),
):
    return db.get(User, trainer.id)


# Review attendance records
@router.get("/attendance")
def review_attendance(
    db: DbSession,
    trainer=Depends(require_role("trainer")),
):
    attendance_records = db.scalars(
        select(Attendance)
        .where(Attendance.trainer_id == trainer.id)
        .order_by(Attendance.id.desc())
    ).all()

    return attendance_records


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

def assign_trainer(
    membership_id: int,
    data: TrainerAssignment,
    db: DbSession,
    admin=Depends(require_role("admin")),
):
    membership = db.get(Membership, membership_id)

    if membership is None:
        raise HTTPException(
            status_code=404,
            detail="Membership not found",
        )

    trainer = db.scalar(
        select(User).where(
            User.id == data.trainer_id,
            User.role == "trainer",
        )
    )

    if trainer is None:
        raise HTTPException(
            status_code=404,
            detail="Trainer not found",
        )

    membership.trainer_id = trainer.id

    db.commit()
    db.refresh(membership)

    return membership
    
