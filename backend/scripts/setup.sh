#!/bin/bash

# TailoRent Setup Script
echo "Setting up TailoRent project..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
echo "Setting up environment..."
cp .env.example .env

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create logs directory
echo "Creating logs directory..."
mkdir -p logs

echo "Setup complete! Run 'python manage.py runserver' to start the development server."
