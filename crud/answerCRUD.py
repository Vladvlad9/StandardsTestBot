from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete, and_

from models import Answers, create_async_session
from schemas import AnswerSchema, AnswerInDBSchema


class CRUDAnswer(object):

    @staticmethod
    @create_async_session
    async def add(answer: AnswerSchema, session: AsyncSession = None) -> AnswerInDBSchema | None:
        answers = Answers(
            **answer.dict()
        )
        session.add(answers)
        try:
            await session.commit()
        except IntegrityError:
            pass
        else:
            await session.refresh(answers)
            return AnswerInDBSchema(**answers.__dict__)

    @staticmethod
    @create_async_session
    async def delete(answer_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(Answers)
            .where(Answers.id == answer_id)
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get(answer_id: int = None, session: AsyncSession = None) -> AnswerInDBSchema | None:
        answer = await session.execute(
            select(Answers)
            .where(Answers.id == answer_id)
        )
        if answers := answer.first():
            return AnswerInDBSchema(**answers[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(session: AsyncSession = None) -> list[AnswerInDBSchema]:
        answers = await session.execute(
            select(Answers)
            .order_by(Answers.id)
        )
        return [AnswerInDBSchema(**answer[0].__dict__) for answer in answers]

    @staticmethod
    @create_async_session
    async def update(answer: AnswerInDBSchema, session: AsyncSession = None) -> None:
        await session.execute(
            update(Answers)
            .where(Answers.id == answer.id)
            .values(**answer.dict())
        )
        await session.commit()
