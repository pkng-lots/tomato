"""update payments table

Revision ID: 2
Revises: 1
Create Date: 2023-07-28 16:17:27.564063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2'
down_revision = '1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('txn_id', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('ins_dttm', sa.DateTime(), nullable=True))
    op.add_column('payments', sa.Column('upd_dttm', sa.DateTime(), nullable=True))
    op.add_column('payments', sa.Column('del_dttm', sa.DateTime(), nullable=True))
    op.add_column('payments', sa.Column('is_del', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_payments_del_dttm'), 'payments', ['del_dttm'], unique=False)
    op.create_index(op.f('ix_payments_ins_dttm'), 'payments', ['ins_dttm'], unique=False)
    op.create_index(op.f('ix_payments_txn_id'), 'payments', ['txn_id'], unique=True)
    op.create_index(op.f('ix_payments_upd_dttm'), 'payments', ['upd_dttm'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_payments_upd_dttm'), table_name='payments')
    op.drop_index(op.f('ix_payments_txn_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_ins_dttm'), table_name='payments')
    op.drop_index(op.f('ix_payments_del_dttm'), table_name='payments')
    op.drop_column('payments', 'is_del')
    op.drop_column('payments', 'del_dttm')
    op.drop_column('payments', 'upd_dttm')
    op.drop_column('payments', 'ins_dttm')
    op.drop_column('payments', 'txn_id')
    # ### end Alembic commands ###
