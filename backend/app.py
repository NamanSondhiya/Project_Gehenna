from flask import Flask, jsonify
from flask_cors import CORS
import os
from connection import coll

app = Flask(__name__)
CORS(app)
PORT = int(os.environ.get('PORT', 8002))

@app.route('/')
def root():
    return jsonify({"status": "ok", "service": "backend"})

@app.route('/api/get')
def get_names():
    names = list(coll.find({}, {"_id": 0, "name": 1}))
    return jsonify([name["name"] for name in names])

@app.route('/add/<name>')
def add_name(name):
    coll.insert_one({"name": name})
    return jsonify({"message": f"'{name}' added successfully!"})

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
