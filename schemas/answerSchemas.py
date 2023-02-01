from pydantic import BaseModel, Field


class AnswerSchema(BaseModel):
    name_answer: str


class AnswerInDBSchema(AnswerSchema):
    id: int = Field(ge=1)


