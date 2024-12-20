from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Import and register blueprint
from backend.routes import jokes_bp
app.register_blueprint(jokes_bp)
