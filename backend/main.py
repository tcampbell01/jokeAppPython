from flask import Flask, request, jsonify
from utils.db import db, app  # Import db and app from utils/db.py
from models import User  # Import User model from models.py

# Create the database tables if they don't exist
@app.before_first_request
def create_tables():
    db.create_all()  # Create tables if not already created

@app.route('/')
def home():
    return "Welcome to the RDS-backed Flask app!"

# Add a new user (POST request)
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()  # Expecting JSON payload
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify(message="Username and email are required!"), 400

    # Check if the user already exists
    if User.query.filter_by(username=username).first():
        return jsonify(message="Username already exists!"), 409

    # Create new user
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User added successfully"), 201

# Get all users (GET request)
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()  # Fetch all users from the database
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(users=user_list)

if __name__ == '__main__':
    app.run(debug=True)  # Running the app in debug mode
