#!/bin/bash

# TailoRent Deployment Script
echo "Deploying TailoRent..."

# Set production environment
export DJANGO_SETTINGS_MODULE=config.settings.production

# Install production dependencies
echo "Installing production dependencies..."
pip install -r requirements/production.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create logs directory
echo "Creating logs directory..."
mkdir -p /var/log/tailorent

# Set proper permissions
echo "Setting permissions..."
chown -R www-data:www-data /var/log/tailorent
chmod -R 755 /var/log/tailorent

echo "Deployment complete!"
