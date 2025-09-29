from flask import Flask, render_template, jsonify
import os
import requests
import logging
from requests.exceptions import RequestException, Timeout, ConnectionError

app = Flask(__name__)
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8002')
PORT = int(os.environ.get('PORT', 8001))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    try:
        response = requests.get(
            f'{BACKEND_URL}/api/get',
            timeout=10,
            headers={'Accept': 'application/json'}
        )
        response.raise_for_status()
        names = response.json()
        if not isinstance(names, list):
            names = []
    except (RequestException, Timeout, ConnectionError) as e:
        logger.error(f"Backend request failed: {str(e)}")
        names = []
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        names = []
    
    return render_template('index.html', data=names, backend_url=BACKEND_URL)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # Use localhost for development, 0.0.0.0 only in containerized environments
    host = '0.0.0.0' if os.environ.get('CONTAINER_ENV') else '127.0.0.1'
    app.run(host=host, port=PORT, debug=False)
