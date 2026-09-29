from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy import func
from app.models import db, Answer, Question
from app.schemas.answers import (
    AnswerRead,
    AnswerCreate, AnswerBase, AnswersList
)
from app.schemas.questions import (
    QuestionResult
)
from app.schemas.errors import error_message, validation_error_response
from .utils import _get_object_or_404

answers_bp = Blueprint(
    "answers",
    __name__,
    url_prefix="/questions/<int:question_id>",
)



@answers_bp.route("/answers", methods=["GET"])
def get_answers(question_id: int):
    question, error = _get_object_or_404(Question, question_id)
    if question is None:
        return error

    answers = db.session.scalars(
        db.select(Answer).where(Answer.question_id == question_id)
    ).all()
    return jsonify(AnswersList.dump_python(answers)), 200


@answers_bp.route('/answers', methods=["POST"])
def create_answer(question_id: int):
    question, error = _get_object_or_404(Question, question_id)
    if question is None:
        return error

    payload = request.get_json()
    if payload is None:
        return error_message(f'Payload is empty', 400)

    try:
        answer = AnswerCreate.model_validate(payload)
    except ValidationError as e:
        return validation_error_response(e)

    answer = Answer(question_id=question_id, is_agree=answer.is_agree)
    db.session.add(answer)
    db.session.commit()
    return jsonify(AnswerRead.model_validate(answer).model_dump()), 201


@answers_bp.route('/results', methods=["GET"])
def get_results(question_id: int):
    question, error = _get_object_or_404(Question, question_id)
    if question is None:
        return error

    res = db.session.execute(
        db.select(Answer.is_agree, func.count(Answer.id))
        .where(Answer.question_id == question_id)
        .group_by(Answer.is_agree)
    )

    counts = {'agree_count': 0, 'disagree_count': 0}
    for is_agree, count in res:
        if is_agree:
            counts['agree_count'] = count
        else:
            counts['disagree_count'] = count

    res = QuestionResult(question_id=question_id, **counts)
    return jsonify(res.model_dump()), 200