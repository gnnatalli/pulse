from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.models import db, Question
from app.schemas.questions import (
    QuestionCreate,
    QuestionRead,
    QuestionUpdate,
    QuestionsList,
)


questions_bp = Blueprint(
    "questions",
    __name__,
    url_prefix="/questions",
)


def _get_question_or_404(question_id: int):
    question = db.session.get(Question, question_id)

    if question is None:
        return None, (
            jsonify({
                "error": f"Question with id={question_id} not found"
            }),
            404,
        )

    return question, None


@questions_bp.route("", methods=["GET"])
def get_questions():
    """Получение списка всех вопросов."""
    questions = db.session.scalars(
        db.select(Question)
    ).all()
    result = QuestionsList.dump_python(questions)
    return jsonify(result), 200


@questions_bp.route("", methods=["POST"])
def create_question():
    """Создание нового вопроса."""
    payload = request.get_json(silent=True)

    if payload is None:
        return jsonify({
            "error": "Invalid or missing JSON body"
        }), 400

    try:
        question_in = QuestionCreate.model_validate(payload)
    except ValidationError as exc:
        return jsonify({
            "error": "Validation error",
            "messages": exc.errors(),
        }), 422

    question = Question(text=question_in.text)
    db.session.add(question)
    db.session.commit()

    return jsonify(
        QuestionRead.model_validate(question).model_dump()
    ), 201


@questions_bp.route("/<int:question_id>", methods=["GET"])
def get_question(question_id: int):
    """Получение конкретного вопроса по ID."""
    question, error = _get_question_or_404(question_id)

    if error:
        return error

    return jsonify(
        QuestionRead.model_validate(question).model_dump()
    ), 200


@questions_bp.route("/<int:question_id>", methods=["PUT"])
def update_question(question_id: int):
    """Обновление конкретного вопроса по ID."""
    question, error = _get_question_or_404(question_id)

    if error:
        return error

    payload = request.get_json(silent=True)

    if payload is None:
        return jsonify({
            "error": "Invalid or missing JSON body"
        }), 400

    try:
        question_in = QuestionUpdate.model_validate(payload)
    except ValidationError as exc:
        return jsonify({
            "error": "Validation error",
            "details": exc.errors(),
        }), 422

    question.text = question_in.text

    db.session.commit()

    return jsonify(
        QuestionRead.model_validate(question).model_dump()
    ), 200


@questions_bp.route("/<int:question_id>", methods=["DELETE"])
def delete_question(question_id: int):
    """Удаление конкретного вопроса по ID."""
    question, error = _get_question_or_404(question_id)

    if error:
        return error

    db.session.delete(question)
    db.session.commit()

    return "", 204