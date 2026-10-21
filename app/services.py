
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Membership, Plan, User


def gym_today() -> date:
    from app.settings import settings
    return datetime.now(ZoneInfo(settings.GYM_TIMEZONE)).date()


def membership_end_date(start_date: date, duration_months: int) -> date:
    # End date is exclusive: the membership is valid before this date.
    return start_date + relativedelta(months=duration_months)


def expire_memberships(db: Session) -> None:
    today = gym_today()

    expired = db.scalars(
        select(Membership).where(
            Membership.is_active.is_(True),
            Membership.end_date <= today,
        )
    ).all()

    for membership in expired:
        membership.is_active = False

    if expired:
        db.commit()


def get_active_membership(db: Session, member_id: int):
    today = gym_today()

    membership = db.scalar(
        select(Membership)
        .where(
            Membership.member_id == member_id,
            Membership.is_active.is_(True),
            Membership.start_date <= today,
            Membership.end_date > today,
        )
        .order_by(Membership.id.desc())
    )

    return membership


def subscribe_member(
    db: Session,
    member_id: int,
    plan_id: int,
) -> Membership:
    expire_memberships(db)

    if get_active_membership(db, member_id):
        raise HTTPException(
            status_code=409,
            detail="You already have an active membership",
        )

    plan = db.get(Plan, plan_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    start = gym_today()

    membership = Membership(
        member_id=member_id,
        plan_id=plan.id,
        start_date=start,
        end_date=membership_end_date(start, plan.duration_months),
        is_active=True,
    )

    db.add(membership)

    try:
        db.commit()
        db.refresh(membership)
    except Exception:
        db.rollback()
        raise

    return membership


def renew_membership(
    db: Session,
    member: User,
    membership_id: int,
) -> Membership:
    expire_memberships(db)

    membership = db.get(Membership, membership_id)

    if not membership or membership.member_id != member.id:
        raise HTTPException(status_code=404, detail="Membership not found")

    if get_active_membership(db, member.id):
        raise HTTPException(
            status_code=409,
            detail="You already have an active membership",
        )

    plan = db.get(Plan, membership.plan_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    start = max(gym_today(), membership.end_date)

    membership.start_date = start
    membership.end_date = membership_end_date(start, plan.duration_months)
    membership.is_active = True

    db.commit()
    db.refresh(membership)

    return membership
