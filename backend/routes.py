from flask import Blueprint, jsonify
from init_db import get_db_connection

jokes_bp = Blueprint('jokes', __name__)


@jokes_bp.route('/api/jokes', methods=['GET'])
def get_jokes():
    try:
        # Get database connection
        conn = get_db_connection()
        print("Database connection established")

        cursor = conn.cursor()

        # Get all jokes
        cursor.execute('SELECT number, category, joke FROM oneliners')
        jokes = cursor.fetchall()

        # Debug: Print raw data
        print(f"Number of jokes fetched: {len(jokes)}")
        print(f"First joke (if any): {jokes[0] if jokes else 'No jokes found'}")

        # Format jokes for JSON response using your exact column names
        jokes_list = []
        for joke in jokes:
            jokes_list.append({
                'number': joke[0],  # matches your 'number' column
                'category': joke[1],  # matches your 'category' column
                'joke': joke[2]  # matches your 'joke' column
            })

        # Debug: Print formatted data
        print(f"Formatted jokes list: {jokes_list}")

        # Close cursor and connection
        cursor.close()
        conn.close()

        return jsonify(jokes_list)

    except Exception as e:
        print(f"Error in get_jokes: {str(e)}")
        return jsonify({'error': str(e)}), 500


@jokes_bp.route('/api/jokes/random', methods=['GET'])
def get_random_joke():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get a random joke - using correct SQL Server syntax
        cursor.execute(
            'SELECT TOP 1 number, category, joke FROM oneliners ORDER BY NEWID()')
        joke = cursor.fetchone()

        if joke:
            joke_data = {
                'number': joke[0],
                'category': joke[1],
                'joke': joke[2]
            }
        else:
            joke_data = {'message': 'No jokes found'}

        cursor.close()
        conn.close()

        return jsonify(joke_data)

    except Exception as e:
        print(f"Error in get_random_joke: {str(e)}")
        return jsonify({'error': str(e)}), 500


@jokes_bp.route('/api/jokes/categories', methods=['GET'])
def get_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT DISTINCT category FROM oneliners')
        categories = [category[0] for category in cursor.fetchall()]

        cursor.close()
        conn.close()

        return jsonify(categories)

    except Exception as e:
        print(f"Error in get_categories: {str(e)}")
        return jsonify({'error': str(e)}), 500


@jokes_bp.route('/api/jokes/category/<category>', methods=['GET'])
def get_jokes_by_category(category):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Using parameterized query for SQL Server
        cursor.execute(
            'SELECT number, category, joke FROM oneliners WHERE category = ?',
            (category,))
        jokes = cursor.fetchall()

        jokes_list = []
        for joke in jokes:
            jokes_list.append({
                'number': joke[0],
                'category': joke[1],
                'joke': joke[2]
            })

        cursor.close()
        conn.close()

        return jsonify(jokes_list)

    except Exception as e:
        print(f"Error in get_jokes_by_category: {str(e)}")
        return jsonify({'error': str(e)}), 500
