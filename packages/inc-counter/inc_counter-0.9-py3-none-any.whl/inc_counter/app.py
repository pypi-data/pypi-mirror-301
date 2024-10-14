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

@app.route('/get_counter', methods=['GET'])
def get_counter():
    global counter
    return jsonify({'counter': counter})

@app.route('/increment', methods=['POST'])
def increment_counter():
    global counter
    counter += 1
    return jsonify({'counter': counter})



@app.route('/reset', methods=['POST'])
def reset_counter():
    global counter
    counter=0
    return jsonify({'counter': counter}) 

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
