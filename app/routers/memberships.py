from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.dependencies import DbSession, require_role
from app.models import Membership, User
from app.schemas import MembershipCreate, MembershipResponse
from app.services import subscribe_member, expire_memberships

router = APIRouter()


@router.get("/trainers")
def get_trainers(
    db: DbSession,
    member=Depends(require_role("member")),
):
    trainers = db.scalars(
        select(User).where(
            User.role == "trainer",
            User.is_active.is_(True),
        )
    ).all()

    return [
        {"id": trainer.id, "name": trainer.name}
        for trainer in trainers
    ]
@router.post("/", response_model=MembershipResponse, status_code=201)
def subscribe(
    data: MembershipCreate,
    db: DbSession,
    member=Depends(require_role("member")),
):
    return subscribe_member(
        db,
        member.id,
        data.plan_id,
        data.trainer_id,  
    )

@router.get("/my", response_model=list[MembershipResponse])
def my_memberships(
    db: DbSession,
    member=Depends(require_role("member")),
):
    expire_memberships(db)

    return db.scalars(
        select(Membership)
        .where(Membership.member_id == member.id)
        .order_by(Membership.id.desc())
    ).all()

@router.patch("/{membership_id}/renew", response_model=MembershipResponse)
def renew(
    membership_id: int,
    db: DbSession,
    member=Depends(require_role("member")),
):
    return renew_membership(db, member, membership_id)
