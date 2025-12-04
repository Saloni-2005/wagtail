#!/usr/bin/env bash
# Build script for Render

set -o errexit  # Exit on error

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r demo/requirements.txt

echo "Installing Wagtail from source..."
pip install -e .

echo "Installing Node dependencies..."
npm ci --no-audit

echo "Building static assets..."
npm run build

echo "Collecting static files..."
cd demo
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate --no-input

echo "Build complete!"
