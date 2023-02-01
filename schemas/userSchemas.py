from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    user_id: int = Field(ge=1)
    fname: str
    lname: str
    mname: str

    restaurant: str
    is_passet: bool
    percent: str

    correct_answer: int
    wrong_answer_selected: list[str]
    wrong_answers: list[str]
    answered_question: list[str]


class UserInDBSchema(UserSchema):
    id: int = Field(ge=1)
