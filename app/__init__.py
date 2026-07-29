from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Registrar Blueprints
    from app.routes.inventory import inventory_bp
    app.register_blueprint(inventory_bp)

    # Endpoint de salud requerido en la Fase 6
    @app.route('/api/health')
    def health_check():
        return {"status": "healthy", "message": "Servidor operando correctamente"}, 200

    return app