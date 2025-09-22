from flask import Flask, request, render_template
import os
import requests


BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8002')
PORT = int(os.environ.get('PORT', 8001))
app = Flask(__name__)

@app.route('/')
def index():
    backend_data = requests.get(f'{BACKEND_URL}/api/get').json()
    print(backend_data)
    
    return render_template('index.html', data=backend_data.get('names', []))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)