from flask import Flask, jsonify, request
import os
import logging
from datetime import datetime
from functools import wraps
from connection import coll, MONGO_URL
import re
from pymongo.errors import PyMongoError, ConnectionFailure
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
PORT = int(os.environ.get('PORT', 8002))
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
app = Flask(__name__)

# Configure Flask app
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

def validate_name(name):
    """Validate name input"""
    if not name or not isinstance(name, str):
        return False, "Name must be a non-empty string"

    if len(name.strip()) == 0:
        return False, "Name cannot be empty or whitespace only"

    if len(name) > 100:
        return False, "Name must be less than 100 characters"

    # Allow alphanumeric characters, spaces, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z0-9\s\-']+$", name):
        return False, "Name contains invalid characters"

    return True, None

def handle_db_errors(f):
    """Decorator to handle database errors"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ConnectionFailure:
            logger.error("Database connection failed")
            return jsonify({
                "error": "Database connection failed",
                "message": "Unable to connect to database"
            }), 503
        except PyMongoError as e:
            logger.error(f"Database error: {e}")
            return jsonify({
                "error": "Database operation failed",
                "message": "A database error occurred"
            }), 500
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {e}")
            return jsonify({
                "error": "Internal server error",
                "message": "An unexpected error occurred"
            }), 500
    return decorated_function

def log_request_info(f):
    """Decorator to log request information"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.info(f"{request.method} {request.path} - {request.remote_addr}")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@log_request_info
def index():
    """Root endpoint"""
    return jsonify({
        "message": "Welcome to the Gehenna Backend API v2.0!",
        "version": "2.0.0",
        "status": "online",
        "endpoints": [
            "/api",
            "/api/get",
            "/api/add/<name>",
            "/health"
        ]
    })

@app.route('/api')
@log_request_info
def api_index():
    """API information endpoint"""
    return jsonify({
        "message": "Gehenna Backend API v2.0",
        "description": "Professional API for name management with MongoDB",
        "version": "2.0.0",
        "documentation": "Available endpoints: GET /api/get, POST /api/add/<name>"
    })

@app.route('/api/get')
@log_request_info
@handle_db_errors
def get_names():
    """Get all names from database"""
    try:
        names = list(coll.find({}, {"_id": 0, "name": 1}))  # Exclude _id field
        result = [name["name"] for name in names]

        logger.info(f"Retrieved {len(result)} names from database")

        return jsonify({
            "names": result,
            "count": len(result),
            "status": "success"
        })

    except Exception as e:
        logger.error(f"Error retrieving names: {e}")
        return jsonify({
            "error": "Failed to retrieve names",
            "message": "Database query failed"
        }), 500

@app.route('/api/add/<name>')
@log_request_info
@handle_db_errors
def add_name(name):
    """Add a new name to database"""
    # Validate input
    is_valid, error_message = validate_name(name)
    if not is_valid:
        logger.warning(f"Invalid name provided: {name} - {error_message}")
        return jsonify({
            "error": "Invalid input",
            "message": error_message
        }), 400

    # Sanitize input
    clean_name = name.strip()

    try:
        # Check if name already exists
        existing = coll.find_one({"name": clean_name})
        if existing:
            logger.info(f"Name '{clean_name}' already exists")
            return jsonify({
                "error": "Name already exists",
                "message": f"The name '{clean_name}' is already in the database"
            }), 409

        # Insert new name
        result = coll.insert_one({"name": clean_name, "created_at": datetime.utcnow()})

        if result.inserted_id:
            logger.info(f"Successfully added name: {clean_name}")
            return jsonify({
                "message": f"'{clean_name}' added successfully!",
                "name": clean_name,
                "id": str(result.inserted_id),
                "status": "success"
            }), 201
        else:
            logger.error("Failed to insert name into database")
            return jsonify({
                "error": "Insertion failed",
                "message": "Failed to save name to database"
            }), 500

    except Exception as e:
        logger.error(f"Error adding name '{clean_name}': {e}")
        return jsonify({
            "error": "Failed to add name",
            "message": "An error occurred while saving the name"
        }), 500

@app.route('/health')
@log_request_info
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        coll.find_one()
        db_status = "healthy"
    except:
        db_status = "unhealthy"

    return jsonify({
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "service": "backend",
        "version": "2.0.0",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
        "environment": {
            "port": PORT,
            "mongo_url": MONGO_URL.replace(MONGO_URL.split('@')[0] if '@' in MONGO_URL else MONGO_URL, "***")
        }
    })

@app.route('/api/stats')
@log_request_info
@handle_db_errors
def get_stats():
    """Get database statistics"""
    try:
        count = coll.count_documents({})
        return jsonify({
            "total_names": count,
            "status": "success"
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({
            "error": "Failed to get statistics",
            "message": "Database query failed"
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "error": "Method not allowed",
        "message": "The HTTP method is not allowed for this endpoint"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    logger.info("Starting Gehenna Backend API v2.0")
    logger.info(f"Port: {PORT}")
    logger.info(f"MongoDB URL: {MONGO_URL.replace(MONGO_URL.split('@')[0] if '@' in MONGO_URL else MONGO_URL, '***')}")

    app.run(
        debug=os.environ.get('DEBUG', 'False').lower() == 'true',
        host='0.0.0.0',
        port=PORT,
        threaded=True
    )
