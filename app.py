from backend import create_app  # Import the app creation function
from flask import Flask


# Create the Flask app instance by calling create_app()
app = create_app()

if __name__ == '__main__':
    app.run()