"""Add image column to project table

Revision ID: 01bcb7bbd735
Revises: 
Create Date: 2025-01-14 00:57:29.330837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01bcb7bbd735'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('author_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['author_id'], ['id'])

    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(length=200), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)

    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_column('image')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['author_id'], ['id'], ondelete='CASCADE')
        batch_op.alter_column('author_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
