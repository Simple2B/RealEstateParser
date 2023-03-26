"""empty message

Revision ID: 96838228a875
Revises: 144711df0303
Create Date: 2023-03-24 14:50:22.871052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96838228a875'
down_revision = '144711df0303'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=256),
               type_=sa.String(length=64),
               existing_nullable=False)
        batch_op.drop_constraint('locations_name_key', type_='unique')

    with op.batch_alter_table('urls', schema=None) as batch_op:
        batch_op.drop_constraint('urls_url_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('urls', schema=None) as batch_op:
        batch_op.create_unique_constraint('urls_url_key', ['url'])

    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.create_unique_constraint('locations_name_key', ['name'])
        batch_op.alter_column('name',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=256),
               existing_nullable=False)

    # ### end Alembic commands ###