
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.dependencies import CurrentUser, DbSession, require_role
from app.models import Membership
from app.schemas import MembershipCreate, MembershipResponse
from app.services import subscribe_member, renew_membership, expire_memberships

router = APIRouter()


@router.post("/", response_model=MembershipResponse, status_code=201)
def subscribe(
    data: MembershipCreate,
    db: DbSession,
    member=Depends(require_role("member")),
):
    return subscribe_member(db, member.id, data.plan_id)


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
