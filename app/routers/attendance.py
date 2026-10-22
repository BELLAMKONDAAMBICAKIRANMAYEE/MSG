from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from app.dependencies import DbSession, require_role
from app.models import Attendance, Membership
from app.schemas import AttendanceCreate, AttendanceResponse, AttendanceReportItem
from app.services import gym_today, get_active_membership
from app.settings import settings

router = APIRouter()



@router.post("/", response_model=AttendanceResponse, status_code=201)
def check_in(
    data: AttendanceCreate,
    db: DbSession,
    trainer=Depends(require_role("trainer")),
):
    membership = get_active_membership(db, data.member_id)

    if not membership:
        raise HTTPException(
            status_code=400,
            detail="Member has no active membership",
        )

    if membership.trainer_id != trainer.id:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this member",
        )

    local_now = datetime.now(ZoneInfo(settings.GYM_TIMEZONE))
    today = local_now.date()

    attendance = Attendance(
        member_id=data.member_id,
        checked_in_at=datetime.now(timezone.utc),
        checked_in_by=trainer.id,
        attendance_date=today,
    )

    db.add(attendance)

    try:
        db.commit()
        db.refresh(attendance)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Member has already checked in today",
        )

    return attendance


@router.get("/my", response_model=list[AttendanceResponse])
def my_attendance(
    db: DbSession,
    member=Depends(require_role("member")),
):
    return db.scalars(
        select(Attendance)
        .where(Attendance.member_id == member.id)
        .order_by(Attendance.checked_in_at.desc())
    ).all()


@router.get("/", response_model=list[AttendanceResponse])
def all_attendance(
    db: DbSession,
    admin=Depends(require_role("admin")),
    start_date: date | None = None,
    end_date: date | None = None,
):
    query = select(Attendance)

    if start_date:
        query = query.where(Attendance.attendance_date >= start_date)

    if end_date:
        query = query.where(Attendance.attendance_date <= end_date)

    return db.scalars(
        query.order_by(Attendance.checked_in_at.desc())
    ).all()


@router.get("/reports/daily", response_model=list[AttendanceReportItem])
def daily_report(
    db: DbSession,
    admin=Depends(require_role("admin")),
    start_date: date | None = None,
    end_date: date | None = None,
):
    query = (
        select(
            Attendance.attendance_date.label("date"),
            func.count(Attendance.id).label("total_checkins"),
        )
        .group_by(Attendance.attendance_date)
        .order_by(Attendance.attendance_date)
    )

    if start_date:
        query = query.where(Attendance.attendance_date >= start_date)

    if end_date:
        query = query.where(Attendance.attendance_date <= end_date)

    rows = db.execute(query).all()

    return [
        {"date": row.date, "total_checkins": row.total_checkins}
        for row in rows
    ]


@router.get("/reports/weekly")
def weekly_report(
    db: DbSession,
    admin=Depends(require_role("admin")),
    start_date: date | None = None,
    end_date: date | None = None,
):
    query = select(
        func.yearweek(Attendance.attendance_date, 3).label("year_week"),
        func.count(Attendance.id).label("total_checkins"),
    ).group_by(
        func.yearweek(Attendance.attendance_date, 3)
    ).order_by(
        func.yearweek(Attendance.attendance_date, 3)
    )

    if start_date:
        query = query.where(Attendance.attendance_date >= start_date)

    if end_date:
        query = query.where(Attendance.attendance_date <= end_date)

    return [
        {"year_week": row.year_week, "total_checkins": row.total_checkins}
        for row in db.execute(query).all()
    ]
