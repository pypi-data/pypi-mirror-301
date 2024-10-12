# backend/assignment_counter/app.py
import logging
from flask import Flask, jsonify, request, send_from_directory,render_template
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

counter = 0


@app.before_request
def log_request_info():
    app.logger.info('Request Path: %s', request.path)

@app.route('/api/increment', methods=['POST'])
def increment_counter():
    global counter
    counter += 1
    return jsonify({'counter': counter})

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

def main():
    app.run(debug=True, port=8000)

if __name__ == "__main__":
    main()
