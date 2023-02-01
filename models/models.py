from datetime import datetime

from sqlalchemy import Column, TIMESTAMP, VARCHAR, Integer, Boolean, Text, ForeignKey, CHAR, BigInteger, SmallInteger, \
    ARRAY, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__: str = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    fname = Column(Text)
    lname = Column(Text)
    mname = Column(Text)
    restaurant = Column(Text)
    is_passet = Column(Boolean)
    correct_answer = Column(Integer)
    wrong_answer_selected = Column(ARRAY(Text))
    wrong_answers = Column(ARRAY(Text))
    answered_question = Column(ARRAY(Text))
    percent = Column(Text)


class Questions(Base):
    __tablename__: str = "questions"

    id: int = Column(Integer, primary_key=True)
    img_id = Column(Integer)
    answer = Column(Text)
    description = Column(Text)


class Answers(Base):
    __tablename__: str = "answers"

    id: int = Column(Integer, primary_key=True)
    name_answer = Column(Text)

