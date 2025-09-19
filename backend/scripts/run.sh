#!/bin/bash
set -e

echo "🚀 Starting TailoRent backend with Celery..."

# Activate virtual environment
source fashion/bin/activate

# Start Django server
echo "Starting Django server on http://127.0.0.1:8000"
python manage.py runserver &

# Start Celery worker
echo "Starting Celery worker..."
celery -A config worker --loglevel=info &

# Start Celery beat scheduler
echo "Starting Celery beat..."
celery -A config beat --loglevel=info &

wait
