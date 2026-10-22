
from datetime import date, datetime
from zoneinfo import ZoneInfo

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Membership, Plan, User


def gym_today() -> date:
    from app.settings import settings

    return datetime.now(
        ZoneInfo(settings.GYM_TIMEZONE)
    ).date()


def membership_end_date(
    start_date: date,
    duration_months: int,
) -> date:
    # The end date is exclusive.
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


def get_active_membership(
    db: Session,
    member_id: int,
):
    today = gym_today()

    return db.scalar(
        select(Membership)
        .where(
            Membership.member_id == member_id,
            Membership.is_active.is_(True),
            Membership.start_date <= today,
            Membership.end_date > today,
        )
        .order_by(Membership.id.desc())
    )


def subscribe_member(
    db: Session,
    member_id: int,
    plan_id: int,
    trainer_id: int,
) -> Membership:

    # 1. Expire memberships whose end date has passed.
    expire_memberships(db)

    # 2. Validate the selected membership plan.
    plan = db.get(Plan, plan_id)

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Plan not found",
        )

    # 3. Validate the selected trainer.
    trainer = db.scalar(
        select(User).where(
            User.id == trainer_id,
            User.role == "trainer",
            User.is_active.is_(True),
        )
    )

    if trainer is None:
        raise HTTPException(
            status_code=404,
            detail="Active trainer not found",
        )

    # 4. Prevent duplicate active memberships for the same plan.
    existing = db.scalar(
        select(Membership).where(
            Membership.member_id == member_id,
            Membership.plan_id == plan_id,
            Membership.is_active.is_(True),
        )
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail=(
                "You already have an active membership "
                "for this plan"
            ),
        )

    # 5. Calculate dates using your existing date helpers.
    today = gym_today()

    end_date = membership_end_date(
        today,
        plan.duration_months,
    )

    # 6. Create the membership with the selected trainer.
    membership = Membership(
        member_id=member_id,
        plan_id=plan_id,
        trainer_id=trainer.id,
        start_date=today,
        end_date=end_date,
        is_active=True,
    )

    try:
        db.add(membership)
        db.commit()
        db.refresh(membership)
        return membership

    except Exception:
        db.rollback()
        raise


def renew_membership(
    db: Session,
    member: User,
    membership_id: int,
) -> Membership:

    expire_memberships(db)

    membership = db.get(Membership, membership_id)

    if not membership or membership.member_id != member.id:
        raise HTTPException(
            status_code=404,
            detail="Membership not found",
        )

    if get_active_membership(db, member.id):
        raise HTTPException(
            status_code=409,
            detail="You already have an active membership",
        )

    plan = db.get(Plan, membership.plan_id)

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Plan not found",
        )

    start = max(gym_today(), membership.end_date)

    membership.start_date = start
    membership.end_date = membership_end_date(
        start,
        plan.duration_months,
    )
    membership.is_active = True

    try:
        db.commit()
        db.refresh(membership)
        return membership

    except Exception:
        db.rollback()
        raise
