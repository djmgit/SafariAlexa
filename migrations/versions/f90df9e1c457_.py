"""empty message

Revision ID: f90df9e1c457
Revises: None
Create Date: 2018-04-06 02:37:01.837811

"""

# revision identifiers, used by Alembic.
revision = 'f90df9e1c457'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Users')
    op.drop_table('Notif')
    op.drop_table('Document')
    op.drop_table('Prebirth')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Prebirth',
    sa.Column('artcile_id', sa.INTEGER(), server_default=sa.text('nextval(\'"Prebirth_artcile_id_seq"\'::regclass)'), nullable=False),
    sa.Column('month_no', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('article', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dos', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('donts', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('diet', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('artcile_id', name='Prebirth_pkey')
    )
    op.create_table('Document',
    sa.Column('document_id', sa.INTEGER(), server_default=sa.text('nextval(\'"Document_document_id_seq"\'::regclass)'), nullable=False),
    sa.Column('filename', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('keywords', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('total_no_stages', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('stages', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('current_no_stage', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('document_id', name='Document_pkey')
    )
    op.create_table('Notif',
    sa.Column('document_id', sa.INTEGER(), server_default=sa.text('nextval(\'"Notif_document_id_seq"\'::regclass)'), nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('query', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('document_id', name='Notif_pkey')
    )
    op.create_table('Users',
    sa.Column('user_id', sa.INTEGER(), server_default=sa.text('nextval(\'"Users_user_id_seq"\'::regclass)'), nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('designation', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('user_id', name='Users_pkey')
    )
    # ### end Alembic commands ###