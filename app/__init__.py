from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes.inventory import inventory_bp
    app.register_blueprint(inventory_bp)

    @app.route('/api/health')
    def health_check():
        return {"status": "healthy", "message": "Servidor operando correctamente"}, 200

    with app.app_context():
        from app import models
        db.create_all()

    return app