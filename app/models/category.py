from app.models import db


class Category(db.Model):
    __tablename__ = "categories"

    id: db.Mapped[int] = db.mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: db.Mapped[str] = db.mapped_column(
        db.String(100),
        nullable=False
    )

    questions: db.Mapped[list["Question"]] = db.relationship(
        back_populates="category"
    )