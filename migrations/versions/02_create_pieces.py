'''empty message

Revision ID: addingpitblu
Revises: 8ffdd60ea201
Create Date: 2021-04-08 19:48:00.000000

'''
from alembic import op
from sqlalchemy import sql
from sqlalchemy.dialects import postgresql

from app import repositories

# 2021-04-08, 19:48.py

revision = 'add_data'
down_revision = 'create_table'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        postgresql.insert(repositories.Piece).values({
            'name': 'KNIGHT',
            'type': 'KNIGHT',
            'color': 'BLACK',
        }))
    op.execute(
        postgresql.insert(repositories.Piece).values({
            'name': 'KNIGHT',
            'type': 'KNIGHT',
            'color': 'WHITE',
        })
    )


def downgrade():
    repositories.Piece.query.filter_by(name='KNIGHT').first().delete()
    repositories.Piece.query.filter_by(name='KNIGHT').first().delete()
