"""create restaurants table

Revision ID: f113a2f0f102
Revises: 
Create Date: 2026-07-03 02:35:59.438228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f113a2f0f102'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'restaurants',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('owner_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('state', sa.String(), nullable=False),
        sa.Column('status', sa.Enum('OPEN', 'CLOSED', 'TEMPORARILY_CLOSED', name='restaurantstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_restaurants_owner_id'), 'restaurants', ['owner_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_restaurants_owner_id'), table_name='restaurants')
    op.drop_table('restaurants')
    sa.Enum(name='restaurantstatus').drop(op.get_bind())
