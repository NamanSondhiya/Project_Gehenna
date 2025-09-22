from flask import Flask, jsonify
import os
from connection import coll, MONGO_URL

PORT = int(os.environ.get('PORT', 8002))
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Gehenna Backend!"})

@app.route('/api')
def api_index():
    return jsonify({"message": "Welcome to the Gehenna Backend API!"})

@app.route('/api/get')
def api():
    
    names = coll.find()

    result = []

    for name in names:
        
        result.append(name['name'])

    result = {
        "names": result
    }
    return jsonify(result)

@app.route('/add/<name>')
def add_name(name):

    coll.insert_one({"name": name})
    
    return jsonify({"message": f"{name} added successfully!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)
