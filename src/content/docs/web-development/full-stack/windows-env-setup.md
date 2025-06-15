---
title: Windows Environment Setup
description: Windows.
---
The following shows the steps to setup development environment on Windows,
including Git, Django, PostgreSQL and Angular
```bash
# Git
ssh-keygen -t rsa

# In Git Bash
cat $HOME/.ssh/id_rsa.pub
# Or
cat $USERPROFILE\\.ssh\\id_rsa.pub
# Or In cmd
type %USERPROFILE%\.ssh\id_rsa.pub

# In Git Bash

# Update git config to avoid File name too long issue when cloning the repo
git config --global core.longpaths true

# Check username
echo $USERNAME
# If $USER not exist or not consistent with user name
export USERNAME=${your_username}


# Django
# Example: if virtualenv_path=%USERPROFILE%\virtualenvs\webapps
mkdir %USERPROFILE%\virtualenvs
# Create venv `webapps`
python -m venv %USERPROFILE%\virtualenvs\webapps

# Activate the virtual environment
.\path\to\venv\Scripts\activate

pip install -r requirements.txt

# Deactivate the env
deactivate


# PostgreSQL
# Open a cmd

# Verify server version
postgres -V

# Verify client version
psql -V

# Go to the postgres folder first
cd \path\to\postgresql\pgsql

# Initialize the database
# It will prompt to enter new superuser password, choose the one you want and remember it
initdb -D mydata -U postgres -W -E UTF8 -A scram-sha-256

# Start the PostgreSQL server
pg_ctl -D mydata -l logfile start

# Start the PostgreSQL interactive shell
# The password is what you set when initializing the db
psql -U postgres

# Add Django user
CREATE ROLE django WITH LOGIN ENCRYPTED PASSWORD 'django';

# Set user's rights
ALTER ROLE django WITH Superuser;

# Create Django database for Django user
CREATE DATABASE django WITH OWNER django ENCODING 'UTF8';

# Create apps-related databases
CREATE DATABASE "django_db" WITH OWNER "django" ENCODING 'UTF-8';

# Displays a list of all databases
\l

# Exit psql
\q


# Frontend
curl /link/to/assets.tar.gz --output assets.tar.gz
# Then extract the assets.tar.gz.You might need to extract twice for a tar.gz file
# Remove the compression file
del assets.tar.gz

cd \path\to\frontend
# Node 14 is required
set PATH=\node\14\path;%PATH%
npm -g install @angular/cli@13.3.9
npm install
```
