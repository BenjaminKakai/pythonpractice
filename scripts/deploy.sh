#!/bin/bash

# Pull latest changes
git pull origin main

# Build and start containers
docker-compose build
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --no-input

# Restart services
docker-compose restart web
