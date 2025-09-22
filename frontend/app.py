from flask import Flask, request, render_template, jsonify
import os
import requests
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8002')
PORT = int(os.environ.get('PORT', 8001))
app = Flask(__name__)

# Custom error pages
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

def handle_backend_errors(f):
    """Decorator to handle backend communication errors"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            logger.error(f"Backend connection error: {BACKEND_URL}")
            return render_template('error.html',
                                 error_code="CONNECTION_ERROR",
                                 error_message="Unable to connect to backend service")
        except requests.exceptions.Timeout:
            logger.error(f"Backend timeout: {BACKEND_URL}")
            return render_template('error.html',
                                 error_code="TIMEOUT",
                                 error_message="Backend service timeout")
        except requests.exceptions.RequestException as e:
            logger.error(f"Backend request error: {e}")
            return render_template('error.html',
                                 error_code="REQUEST_ERROR",
                                 error_message="Backend service error")
    return decorated_function

@app.route('/')
@handle_backend_errors
def index():
    """Main dashboard route"""
    try:
        # Check backend health first
        health_response = requests.get(f'{BACKEND_URL}/api', timeout=5)
        backend_healthy = health_response.status_code == 200
    except:
        backend_healthy = False

    try:
        # Get data from backend
        if backend_healthy:
            backend_data = requests.get(f'{BACKEND_URL}/api/get', timeout=10).json()
            names = backend_data.get('names', [])
            logger.info(f"Successfully retrieved {len(names)} names from backend")
        else:
            names = []
            logger.warning("Backend not healthy, returning empty data")
    except Exception as e:
        logger.error(f"Error fetching data from backend: {e}")
        names = []

    return render_template('index.html',
                         data=names,
                         backend_url=BACKEND_URL,
                         backend_healthy=backend_healthy)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "frontend",
        "backend_url": BACKEND_URL,
        "version": "2.0.0"
    })

@app.route('/api/status')
def api_status():
    """Get backend API status"""
    try:
        response = requests.get(f'{BACKEND_URL}/api', timeout=5)
        return jsonify({
            "backend_status": "online" if response.status_code == 200 else "offline",
            "response_time": response.elapsed.total_seconds() * 1000,  # in milliseconds
            "status_code": response.status_code
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "backend_status": "offline",
            "error": str(e)
        })

if __name__ == '__main__':
    logger.info(f"Starting Gehenna Frontend v2.0 on port {PORT}")
    logger.info(f"Backend URL: {BACKEND_URL}")

    app.run(
        debug=os.environ.get('DEBUG', 'False').lower() == 'true',
        host='0.0.0.0',
        port=PORT,
        threaded=True
    )
