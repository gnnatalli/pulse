from pydantic import BaseModel, ValidationError
from flask import jsonify


class ErrorResponse(BaseModel):
    error: str
    details: list = []

def error_message(message: str, status_code: int, details: list | None = None):
    payload = ErrorResponse(error=message, details=details)
    return jsonify(payload.model_dump()), status_code


def validation_error_response(exc: ValidationError, status_code: int):
    payload = ErrorResponse(error='Validation Error', details=exc.errors(include_url=False, include_context=False))
    return jsonify(payload.model_dump()), status_code