"""add answer

Revision ID: 01587a6cb5f0
Revises: 7248c61118e7
Create Date: 2023-02-01 20:33:51.605757

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session


# revision identifiers, used by Alembic.
from models import create_sync_session, Answers
from sqlalchemy.exc import IntegrityError

revision = '01587a6cb5f0'
down_revision = '7248c61118e7'
branch_labels = None
depends_on = None

answers = ['L1', 'L3', 'Стандарты бренда', 'Нет правильного ответа', 'Не является отклонением']


@create_sync_session
def upgrade(session: Session = None) -> None:
    for answer in answers:
        _answer = Answers(name_answer=answer)
        session.add(_answer)
        try:
            session.commit()
        except IntegrityError:
            pass


@create_sync_session
def downgrade(session: Session = None) -> None:
    for answer in answers:
        session.execute(
            sa.delete(Answers)
            .where(Answers.name_answer == answer)
        )
        session.commit()
