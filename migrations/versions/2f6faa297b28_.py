"""empty message

Revision ID: 2f6faa297b28
Revises: 
Create Date: 2019-08-06 13:35:00.095833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f6faa297b28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('maintenance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider_maintenance_id', sa.String(length=128), nullable=True),
    sa.Column('start', sa.TIME(), nullable=True),
    sa.Column('end', sa.TIME(), nullable=True),
    sa.Column('timezone', sa.String(length=128), nullable=True),
    sa.Column('cancelled', sa.INTEGER(), nullable=True),
    sa.Column('rescheduled', sa.INTEGER(), nullable=True),
    sa.Column('rescheduled_id', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=2048), nullable=True),
    sa.Column('reason', sa.TEXT(), nullable=True),
    sa.Column('received_dt', sa.DateTime(), nullable=True),
    sa.Column('started', sa.INTEGER(), nullable=True),
    sa.Column('ended', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['rescheduled_id'], ['maintenance.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_maintenance_location'), 'maintenance', ['location'], unique=False)
    op.create_table('provider',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('type', sa.Enum('transit', 'backbone', 'transport', 'peering', 'facility', 'multi', name='ProviderType'), nullable=True),
    sa.Column('email_esc', sa.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_name'), 'provider', ['name'], unique=False)
    op.create_table('circuit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider_cid', sa.VARCHAR(length=128), nullable=True),
    sa.Column('a_side', sa.VARCHAR(length=128), nullable=True),
    sa.Column('z_side', sa.VARCHAR(length=128), nullable=True),
    sa.Column('provider_id', sa.Integer(), nullable=True),
    sa.Column('contract_filename', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_circuit_provider_cid'), 'circuit', ['provider_cid'], unique=True)
    op.create_table('maint_update',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('maintenance_id', sa.Integer(), nullable=True),
    sa.Column('comment', sa.TEXT(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['maintenance_id'], ['maintenance.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('maint_circuit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('maint_id', sa.Integer(), nullable=True),
    sa.Column('circuit_id', sa.Integer(), nullable=True),
    sa.Column('impact', sa.VARCHAR(length=128), nullable=True),
    sa.Column('date', sa.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['circuit_id'], ['circuit.id'], ),
    sa.ForeignKeyConstraint(['maint_id'], ['maintenance.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_apscheduler_jobs_next_run_time', table_name='apscheduler_jobs')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_apscheduler_jobs_next_run_time', 'apscheduler_jobs', ['next_run_time'], unique=False)
    op.drop_table('maint_circuit')
    op.drop_table('maint_update')
    op.drop_index(op.f('ix_circuit_provider_cid'), table_name='circuit')
    op.drop_table('circuit')
    op.drop_index(op.f('ix_provider_name'), table_name='provider')
    op.drop_table('provider')
    op.drop_index(op.f('ix_maintenance_location'), table_name='maintenance')
    op.drop_table('maintenance')
    # ### end Alembic commands ###
