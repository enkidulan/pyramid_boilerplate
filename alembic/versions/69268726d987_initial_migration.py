"""Initial migration

Revision ID: 69268726d987
Revises: 
Create Date: 2016-04-23 00:27:44.898496

"""

# revision identifiers, used by Alembic.
revision = '69268726d987'
down_revision = None
branch_labels = None
depends_on = None

import datetime
import websauna.system.model.columns
from sqlalchemy.types import Text  # Needed from proper creation of JSON fields as Alembic inserts astext_type=Text() row

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('created_at', websauna.system.model.columns.UTCDateTime(), nullable=True),
    sa.Column('updated_at', websauna.system.model.columns.UTCDateTime(), nullable=True),
    sa.Column('group_data', postgresql.JSONB(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_group')),
    sa.UniqueConstraint('name', name=op.f('uq_group_name'))
    )
    op.create_table('user_activation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', websauna.system.model.columns.UTCDateTime(), nullable=True),
    sa.Column('updated_at', websauna.system.model.columns.UTCDateTime(), nullable=True),
    sa.Column('expires_at', websauna.system.model.columns.UTCDateTime(), nullable=False),
    sa.Column('code', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_activation')),
    sa.UniqueConstraint('code', name=op.f('uq_user_activation_code'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('username', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=True),
    sa.Column('created_at', websauna.system.model.columns.UTCDateTime(), nullable=True),
    sa.Column('updated_at', websauna.system.model.columns.UTCDateTime(), nullable=True),
    sa.Column('activated_at', websauna.system.model.columns.UTCDateTime(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.Column('last_login_at', websauna.system.model.columns.UTCDateTime(), nullable=True),
    sa.Column('last_login_ip', postgresql.INET(), nullable=True),
    sa.Column('user_data', postgresql.JSONB(), nullable=True),
    sa.Column('last_auth_sensitive_operation_at', websauna.system.model.columns.UTCDateTime(), nullable=True),
    sa.Column('activation_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['activation_id'], ['user_activation.id'], name=op.f('fk_users_activation_id_user_activation')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email')),
    sa.UniqueConstraint('username', name=op.f('uq_users_username'))
    )
    op.create_table('usergroup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], name=op.f('fk_usergroup_group_id_group')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_usergroup_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_usergroup'))
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usergroup')
    op.drop_table('users')
    op.drop_table('user_activation')
    op.drop_table('group')
    ### end Alembic commands ###
