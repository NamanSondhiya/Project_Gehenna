#!/bin/bash

python -m venv venv
source venv/bin/activate

# Run tests for backend
echo "Running backend tests..."
cd backend
pip install -r requirements.txt
python -m pytest tests/test_app.py --cov=app --cov=connection --cov-report=xml:coverage.xml --cov-report=html --junitxml=test-results.xml

# Run tests for frontend
echo "Running frontend tests..."
cd ../frontend
pip install -r requirements.txt
python -m pytest tests/test_app.py --cov=app --cov-report=xml:coverage.xml --cov-report=html --junitxml=test-results.xml

cd ..

echo "Tests completed."
