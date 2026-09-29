from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Импортируем все модели для регистрации в метаданных

from .category import Category
from .questions import Question
from .answers import Answer


