from app.models import db


class Question(db.Model):
    __tablename__ = 'questions'

    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    text: db.Mapped[str] = db.mapped_column(db.String(255))

    category_id: db.Mapped[int] = db.mapped_column(
        db.ForeignKey("categories.id")
    )

    category: db.Mapped["Category"] = db.relationship(
        back_populates="questions"
    )

    answers: db.Mapped[list["Answer"]] = db.relationship(
        back_populates="question",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Question {self.id}: {self.text}>"