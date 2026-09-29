from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, StringConstraints, TypeAdapter


class AnswerBase(BaseModel):
    pass


class AnswerCreate(AnswerBase):
    is_agree: Annotated[bool, Field(strict=True)]


class AnswerRead(AnswerBase):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    is_agree: bool
    question_id: int


AnswersList = TypeAdapter(list[AnswerRead])
