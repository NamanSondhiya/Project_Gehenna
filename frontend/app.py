from flask import Flask, render_template, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8002')
PORT = int(os.environ.get('PORT', 8001))
HOST = os.environ.get('HOST', '0.0.0.0')

@app.route('/')
def index():
    try:
        response = requests.get(f'{BACKEND_URL}/api/get')
        names = response.json()
    except:
        names = []
    return render_template('index.html', data=names)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
