"""empty message

Revision ID: e44cf762ca03
Revises: bf200b0a56d9
Create Date: 2025-07-16 23:01:53.550438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e44cf762ca03'
down_revision = 'bf200b0a56d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('controle_mensal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('professor_id', sa.UUID(), nullable=False))
        batch_op.create_foreign_key(None, 'professor', ['professor_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('controle_mensal', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('professor_id')

    # ### end Alembic commands ###
