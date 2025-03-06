from flask import Flask
from flask_cors import CORS
from backend import create_app


app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}})
if __name__ == "__main__":
    app.run(debug=True, port=25565, host='0.0.0.0')
