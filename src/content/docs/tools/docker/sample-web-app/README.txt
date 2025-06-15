# Docker Web Application Setup

This directory contains Docker configurations for setting up a full-stack web application environment with Django and Angular. The main components include:

- **init.sql**: SQL script for initializing PostgreSQL databases and creating Django roles
- **Dockerfile**: Defines the container environment for the Django backend
- **docker-compose.yml**: Orchestrates multiple services (Django, Angular, PostgreSQL)
- **docker-django-migrate.sh**: Script for database migrations and superuser creation
- **env.py**: Django database configuration settings

## Key Features
- PostgreSQL database initialization with multiple databases
- Django backend with automatic migrations and test data loading
- Angular frontend with hot-reloading development server
- Pre-configured database roles and test database setup
- Health checks and dependency management for services

## Usage
1. Build the Docker containers: `docker-compose build`
2. Start the services: `docker-compose up`
3. Access the applications:
   - Django backend: `http://localhost:8000`
   - Angular frontend: `http://localhost:4200`
4. Database access: `localhost:5433` (PostgreSQL)

Note: The Django container automatically handles database migrations and creates an admin user (username: 'admin', password: 'admin').
