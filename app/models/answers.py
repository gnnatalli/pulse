from app.models import db


class Answer(db.Model):
    __tablename__ = 'answers'

    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    question_id: db.Mapped[int] = db.mapped_column(db.ForeignKey('questions.id'))
    is_agree: db.Mapped[bool]

    question: db.Mapped["Question"] = db.relationship(back_populates="answers")

    def __repr__(self):
        return f"<Answer {self.id}: question={self.question_id}, is_agree={self.is_agree}>"