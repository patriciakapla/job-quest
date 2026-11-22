"""add 'on delete set null' on resume´s FK in applications table

Revision ID: a4a82a329d61
Revises: ab138563e105
Create Date: 2026-11-22 16:33:33.082819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4a82a329d61'
down_revision: Union[str, Sequence[str], None] = 'ab138563e105'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('applications_resume_id_fkey'), 'applications', type_='foreignkey')
    op.create_foreign_key(None, 'applications', 'resumes', ['resume_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'applications', type_='foreignkey') #type: ignore
    op.create_foreign_key(op.f('applications_resume_id_fkey'), 'applications', 'resumes', ['resume_id'], ['id'])
