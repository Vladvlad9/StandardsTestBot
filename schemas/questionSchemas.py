from pydantic import BaseModel, Field


class QuestionSchema(BaseModel):
    img_id: int = Field(ge=1)
    answer: str
    description: str


class QuestionInDBSchema(QuestionSchema):
    id: int = Field(ge=1)
