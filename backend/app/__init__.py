from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Application factory function"""
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config.Config')
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)  # Add this line
    CORS(app)
    
    # Import and register routes
    with app.app_context():
        from app import routes
        
        # Register blueprints or routes
        app.register_blueprint(routes.bp)
        
    return app
