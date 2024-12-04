from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Importar y registrar rutas
    with app.app_context():
        from .routes import register_routes
        register_routes(app)

    return app
