"""empty message

Revision ID: 1de54945ca9b
Revises: 
Create Date: 2021-04-08 11:31:23.189405

"""
from alembic import op
import sqlalchemy as sa
import app
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'create_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table('teste_chessboard',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('positions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
                    sa.Column('possibilities', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('teste_pieces',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('color', sa.String(), nullable=False),
                    sa.Column('type', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teste_chessboard')
    op.drop_table('teste_pieces')
    # ### end Alembic commands ###
