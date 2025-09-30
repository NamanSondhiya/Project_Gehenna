import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import re
from connection import coll

app = Flask(__name__)
CORS(app, origins=["http://localhost:8001", "http://frontend:8001"])  # Limit origins for security
PORT = int(os.environ.get('PORT', 8002))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_name(name):
    """Validate name input: not empty, alphanumeric + spaces, max 50 chars"""
    if not name or not isinstance(name, str):
        return False, "Name is required and must be a string"
    name = name.strip()
    if len(name) == 0 or len(name) > 50:
        return False, "Name must be between 1 and 50 characters"
    if not re.match(r'^[a-zA-Z\s]+$', name):
        return False, "Name can only contain letters and spaces"
    return True, name

@app.route('/')
def root():
    logger.info("Root endpoint accessed")
    return jsonify({"status": "ok", "service": "backend"})

@app.route('/api/get')
def get_names():
    try:
        names = list(coll.find({}, {"_id": 0, "name": 1}))
        names_list = [name["name"] for name in names]
        logger.info(f"Retrieved {len(names_list)} names")
        return jsonify(names_list)
    except Exception as e:
        logger.error(f"Error retrieving names: {str(e)}")
        return jsonify({"error": "Failed to retrieve names"}), 500

@app.route('/api/add/<name>', methods=['POST'])
def add_name(name):
    try:
        valid, cleaned_name = validate_name(name)
        if not valid:
            logger.warning(f"Invalid name attempt: {name} - {cleaned_name}")
            return jsonify({"error": cleaned_name}), 400

        # Check if name already exists
        if coll.find_one({"name": cleaned_name}):
            logger.warning(f"Duplicate name attempt: {cleaned_name}")
            return jsonify({"error": "Name already exists"}), 409

        coll.insert_one({"name": cleaned_name})
        logger.info(f"Added name: {cleaned_name}")
        return jsonify({"message": f"'{cleaned_name}' added successfully!"})
    except Exception as e:
        logger.error(f"Error adding name: {str(e)}")
        return jsonify({"error": "Failed to add name"}), 500

@app.route('/api/delete/<name>', methods=['DELETE'])
def delete_name(name):
    try:
        valid, cleaned_name = validate_name(name)
        if not valid:
            logger.warning(f"Invalid name for deletion: {name} - {cleaned_name}")
            return jsonify({"error": cleaned_name}), 400

        result = coll.delete_one({"name": cleaned_name})
        if result.deleted_count == 0:
            logger.warning(f"Name not found for deletion: {cleaned_name}")
            return jsonify({"error": "Name not found"}), 404

        logger.info(f"Deleted name: {cleaned_name}")
        return jsonify({"message": f"'{cleaned_name}' deleted successfully!"})
    except Exception as e:
        logger.error(f"Error deleting name: {str(e)}")
        return jsonify({"error": "Failed to delete name"}), 500

@app.route('/api/search/<query>')
def search_names(query):
    try:
        if not query or not isinstance(query, str):
            return jsonify({"error": "Query is required"}), 400

        query = query.strip()
        regex = re.compile(query, re.IGNORECASE)
        names = list(coll.find({"name": {"$regex": regex}}, {"_id": 0, "name": 1}))
        names_list = [name["name"] for name in names]
        logger.info(f"Searched for '{query}', found {len(names_list)} results")
        return jsonify(names_list)
    except Exception as e:
        logger.error(f"Error searching names: {str(e)}")
        return jsonify({"error": "Failed to search names"}), 500

@app.route('/health')
def health():
    try:
        # Check database connection
        coll.find_one()
        return jsonify({"status": "ok", "database": "connected"})
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "error", "database": "disconnected"}), 503

if __name__ == '__main__':
    logger.info("Starting backend server")
    app.run(host='0.0.0.0', port=PORT)
