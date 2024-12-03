"""add admin flag

Revision ID: add_admin_flag
Revises: 
Create Date: 2023-11-08 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_admin_flag'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add is_admin column to user table
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=True, server_default='0'))

def downgrade():
    # Remove is_admin column from user table
    op.drop_column('user', 'is_admin')
