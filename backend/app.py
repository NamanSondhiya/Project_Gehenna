from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import logging
from connection import get_collection

app = Flask(__name__)
CORS(app)
PORT = int(os.environ.get('PORT', 8002))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def root():
    return jsonify({"status": "ok", "service": "backend"})

@app.route('/api/get')
def get_names():
    try:
        coll = get_collection()
        if not coll:
            return jsonify({"error": "Database connection failed"}), 500
        
        # Use cursor iteration for better performance
        names = []
        for doc in coll.find({}, {"_id": 0, "name": 1}).limit(1000):
            if "name" in doc:
                names.append(doc["name"])
        
        return jsonify(names)
    except Exception as e:
        logger.error(f"Error retrieving names: {str(e)}")
        return jsonify({"error": "Failed to retrieve data"}), 500

@app.route('/api/add', methods=['POST'])
def add_name():
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
        
        name = data['name'].strip()
        if not name or len(name) > 100:
            return jsonify({"error": "Name must be 1-100 characters"}), 400
        
        # Basic input sanitization
        if any(char in name for char in ['<', '>', '&', '"', "'"]):
            return jsonify({"error": "Name contains invalid characters"}), 400
        
        coll = get_collection()
        if not coll:
            return jsonify({"error": "Database connection failed"}), 500
        
        # Check for duplicates
        if coll.find_one({"name": name}):
            return jsonify({"error": "Name already exists"}), 409
        
        coll.insert_one({"name": name})
        logger.info(f"Added name: {name}")
        return jsonify({"message": f"'{name}' added successfully!"})
    except Exception as e:
        logger.error(f"Error adding name: {str(e)}")
        return jsonify({"error": "Failed to add name"}), 500

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # Use localhost for development, 0.0.0.0 only in containerized environments
    host = '0.0.0.0' if os.environ.get('CONTAINER_ENV') else '127.0.0.1'
    app.run(host=host, port=PORT, debug=False)
