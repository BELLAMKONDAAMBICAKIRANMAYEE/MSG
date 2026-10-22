from typing import Literal
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Literal["admin", "trainer", "member"] = "member"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PlanCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    duration_months: int = Field(gt=0, le=120)
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    description: str | None = None


class PlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    duration_months: int
    price: Decimal
    description: str | None

class MembershipCreate(BaseModel):
    plan_id: int = Field(gt=0)
    trainer_id: int | None = Field(default=None, gt=0)


class MembershipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    plan_id: int
    trainer_id: int | None
    start_date: date
    end_date: date
    is_active: bool


class TrainerAssignment(BaseModel):
    trainer_id: int = Field(gt=0)  


class AttendanceCreate(BaseModel):
    member_id: int


class AttendanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    checked_in_at: date
    # checked_in_by: int
    # attendance_date: date

    model_config = ConfigDict(from_attributes=True)
class AttendanceReportItem(BaseModel):
    date: date
    total_checkins: int
