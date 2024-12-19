# backend/routes.py
from flask import jsonify, request
from . import db
from .models import User
from sqlalchemy.exc import SQLAlchemyError

# This function registers routes with the Flask app
def init_routes(app):
    # Home route
    @app.route('/')
    def home_page():
        return "Welcome to the Flask app!"

    # Add user route (POST request)
    @app.route('/add_user', methods=['POST'])
    def add_user_entry():
        # Get JSON data from the request
        data = request.get_json()
        if not data or not data.get('username') or not data.get('email'):
            return jsonify(message="Missing fields: username and email"), 400

        # Extract data from request
        username = data['username']
        email = data['email']

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify(message="Username already exists!"), 409

        # Create new user
        try:
            new_user = User(username=username, email=email)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(message="User added successfully"), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify(message="Database error occurred!", error=str(e)), 500

    # Get all users route (GET request)
    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return jsonify(users=user_list)
