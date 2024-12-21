from flask import Flask, jsonify, request
from flask_cors import CORS
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'server': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'username': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD')
}


def get_db_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_CONFIG['server']},{DB_CONFIG['port']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        "TrustServerCertificate=yes"
    )
    return pyodbc.connect(conn_str)


# Single joke endpoint
@app.route('/api/joke')
def get_random_joke():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT TOP 1 joke, category FROM oneliners ORDER BY NEWID()")
        joke = cursor.fetchone()
        conn.close()

        if joke:
            return jsonify({
                'joke': joke[0],
                'category': joke[1]
            })
        return jsonify({'error': 'No jokes found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Multiple jokes endpoint - supports both GET and POST
@app.route('/api/jokes', methods=['GET', 'POST'])
def get_multiple_jokes():
    try:
        # Handle both POST and GET methods
        if request.method == 'POST':
            data = request.get_json()
            count = data.get('count', 10) if data else 10
        else:  # GET method
            count = 10  # default value for GET

        # Limit maximum number of jokes
        count = min(count, 50)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT TOP {count} joke, category FROM oneliners ORDER BY NEWID()")
        jokes = cursor.fetchall()
        conn.close()

        if jokes:
            return jsonify({
                'jokes': [
                    {
                        'joke': joke[0],
                        'category': joke[1]
                    } for joke in jokes
                ],
                'count': len(jokes)
            })
        return jsonify({'error': 'No jokes found'}), 404

    except Exception as e:
        print(f"Error: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
