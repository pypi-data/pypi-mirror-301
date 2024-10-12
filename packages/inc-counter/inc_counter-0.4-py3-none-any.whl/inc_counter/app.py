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

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    print("Serving from static folder:", app.static_folder)
    print("Files in build directory:", os.listdir(app.static_folder))
    # If the path is a file in the build/static folder, serve it
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # Otherwise, serve the index.html (for React Router handling other paths)
    else:
        return render_template( 'index.html')

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
