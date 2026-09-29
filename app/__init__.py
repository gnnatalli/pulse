import os

from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.routers import questions_bp, answers_bp

CONFIG_MAP = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig',
}

migrate = Migrate()

def create_app(config_object=None):
    app = Flask(__name__)

    if config_object is None:
        mode = os.environ.get('APP_ENV', 'development')
        config_object = CONFIG_MAP[mode]

    app.config.from_object(config_object)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(questions_bp)
    app.register_blueprint(answers_bp)

    return app