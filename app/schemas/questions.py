from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, StringConstraints, TypeAdapter, computed_field


QuestionText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=5,
        max_length=100)
]

CategoryName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=100)
]


class CategoryBase(BaseModel):
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=100
        )
    ]


class QuestionBase(BaseModel):
    text: QuestionText


class QuestionCreate(QuestionBase):
    category_id: int


class QuestionUpdate(QuestionBase):
    text: QuestionText | None = None
    category_id: int | None = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    
class QuestionRead(QuestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: CategoryRead


QuestionsList = TypeAdapter(list[QuestionRead])


class QuestionResult(BaseModel):
    question_id: int
    agree_count: int
    disagree_count: int

    @computed_field
    @property
    def total(self) -> int:
        return self.agree_count + self.disagree_count


    @computed_field
    @property
    def is_agree_percentage(self) -> float:
        if not self.total:
            return 0.0
        return round(self.agree_count / self.total * 100, 2)