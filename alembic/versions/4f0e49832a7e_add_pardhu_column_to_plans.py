"""add pardhu column to plans

Revision ID: 4f0e49832a7e
Revises: 
Create Date: 2026-10-23 15:59:02.345398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '4f0e49832a7e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('plans', sa.Column('pardhu', mysql.TEXT(), nullable=True))
   


