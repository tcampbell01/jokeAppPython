from flask import Flask
from dotenv import load_dotenv
import os
from utils.db import db  # Import the db instance
from .init_db import create_tables  # Import the create_tables function

def create_app():
    """Create and configure the Flask app"""

    # Load environment variables from .env file
    load_dotenv()

    # Create Flask app
    app = Flask(__name__)

    # Configure the app (set up the database URI from .env or default to sqlite)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///yourdatabase.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Flag to check if initialization has been done
    app.initialized = False

    @app.before_request
    def initialize():
        if not app.initialized:
            with app.app_context():
                create_tables()  # Run table creation logic
                app.initialized = True

    # Import and register routes
    from .routes import init_routes
    init_routes(app)

    return app