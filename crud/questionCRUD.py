from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete, and_

from models import Questions, create_async_session
from schemas import QuestionSchema, QuestionInDBSchema


class CRUDQuestions(object):

    @staticmethod
    @create_async_session
    async def get(question_id: int, session: AsyncSession = None) -> QuestionInDBSchema | None:
        questions = await session.execute(
            select(Questions)
            .where(Questions.id == question_id)
        )
        if question := questions.first():
            return QuestionInDBSchema(**question[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(session: AsyncSession = None) -> list[QuestionInDBSchema]:
        questions = await session.execute(
            select(Questions)
            .order_by(Questions.id)
        )
        return [QuestionInDBSchema(**question[0].__dict__) for question in questions]

    @staticmethod
    @create_async_session
    async def get_question_and_answer(question_id: int,
                                      answer_id: int,
                                      session: AsyncSession = None) -> QuestionInDBSchema | None:
        questions = await session.execute(
            select(Questions)
            .where(Questions.id == question_id, and_(Questions.answer == str(answer_id)))
        )
        if question := questions.first():
            return QuestionInDBSchema(**question[0].__dict__)

