"""create table

Revision ID: 7248c61118e7
Revises: 
Create Date: 2023-02-01 15:08:25.351042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7248c61118e7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),

                    sa.Column('fname', sa.Text()),
                    sa.Column('lname', sa.Text()),
                    sa.Column('mname', sa.Text()),

                    sa.Column('restaurant', sa.Text()),
                    sa.Column('is_passet', sa.Boolean()),
                    sa.Column('percent', sa.Text()),

                    sa.Column('correct_answer', sa.Integer()),
                    sa.Column('wrong_answer_selected', sa.ARRAY(sa.Text)),
                    sa.Column('wrong_answers', sa.ARRAY(sa.Text)),
                    sa.Column('answered_question', sa.ARRAY(sa.Text)),

                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('questions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('img_id', sa.Integer()),

                    sa.Column('answer', sa.Text()),
                    sa.Column('description', sa.Text()),

                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('answers',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name_answer', sa.Text()),

                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('questions')
    op.drop_table('answers')
