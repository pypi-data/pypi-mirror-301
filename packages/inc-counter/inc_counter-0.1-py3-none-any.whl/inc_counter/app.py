# backend/assignment_counter/app.py
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../../frontend/build', static_url_path='')
CORS(app)

counter = 0

@app.route('/api/increment', methods=['POST'])
def increment_counter():
    global counter
    counter += 1
    return jsonify({'counter': counter})

@app.route('/')
def serve_frontend():
    print("Serving from static folder:", app.static_folder)
    print("Files in build directory:", os.listdir(app.static_folder))
    return send_from_directory(app.static_folder, 'index.html')

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
