"""add unique constraint on salary.vacancy_id

Revision ID: 5d6c956d9317
Revises: 8195994b55bc
Create Date: 2026-10-08 22:39:21.970396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d6c956d9317'
down_revision: Union[str, Sequence[str], None] = '8195994b55bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        'uq_salary_vacancy', 'salary', ['vacancy_id'], schema='hh'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_salary_vacancy', 'salary', type_='unique', schema='hh')
