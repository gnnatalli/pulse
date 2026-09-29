from app.models import db
from app.models import Question, Answer
from app.schemas.errors import error_message

def _get_object_or_404(model, pk):
    obj = db.session.get(model, pk)
    if obj is None:
        return None, error_message(f'{model.__name__} with id {pk} not found', 404)
    return obj, None