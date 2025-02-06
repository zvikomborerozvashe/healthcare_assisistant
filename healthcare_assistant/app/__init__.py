from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database with Flask app
    db.init_app(app)

    # Import and register routes (to avoid circular imports)
    from app.routes import main
    app.register_blueprint(main)

    return app
