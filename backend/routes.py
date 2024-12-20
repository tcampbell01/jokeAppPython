from flask import Blueprint, jsonify
from init_db import get_db_connection

jokes_bp = Blueprint('jokes', __name__)


@jokes_bp.route('/api/jokes', methods=['GET'])
def get_jokes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM oneliners')
        jokes = cursor.fetchall()

        jokes_list = []
        for joke in jokes:
            jokes_list.append({
                'number': joke[0],
                'category': joke[1],
                'joke': joke[2]
            })

        return jsonify(jokes_list)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@jokes_bp.route('/api/jokes/random', methods=['GET'])
def get_random_joke():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT TOP 1 * FROM oneliners ORDER BY NEWID()')
        joke = cursor.fetchone()

        if joke:
            return jsonify({
                'number': joke[0],
                'category': joke[1],
                'joke': joke[2]
            })
        return jsonify({'message': 'No jokes found'}), 404
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@jokes_bp.route('/api/jokes/random', methods=['GET'])  # Added /api prefix
def get_random_joke():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT TOP 1 * FROM oneliners ORDER BY NEWID()')
        joke = cursor.fetchone()

        if joke:
            return jsonify({
                'id': joke[0],
                'joke_text': joke[1]
            })
        return jsonify({'message': 'No jokes found'}), 404
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
