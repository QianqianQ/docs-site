---
title: PostgreSQL
description: PostgreSQL.
---

## Installation
```bash
# Install dependencies
sudo apt-get install -y postgresql postgresql-contrib

# Verify server version
postgres -V
# In the event that the postgres command is not found, you may need to locate the directory of the utility: locate bin/postgres
# If not work
sudo -u postgres psql -c 'SELECT version();'

# Verify client verion
psql --version
psql -V

# Possibly configure system locales
# Reconfigure system locales to set default language and character encoding
# This is important for PostgreSQL as it affects database encoding and sorting
sudo dpkg-reconfigure locales

# Switch to the postgres user
sudo su - postgres
sudo -u postgres -i
# Both commands switch to the postgres user, but with different approaches:
# 1. 'sudo su - postgres' - Starts a new login shell as postgres user
# 2. 'sudo -u postgres -i' - Runs an interactive shell as postgres user
# The main differences are:
# - 'su -' changes the entire environment to the target user
# - '-i' with sudo provides a more limited environment
# - 'su -' requires the target user's password (if root password is not set)
# - 'sudo -u' uses the current user's sudo privileges

# View all user accounts and their authentication details in PostgreSQL
# pg_shadow is a system catalog table that stores user account information
# including usernames, password hashes, and account privileges
select * from pg_shadow;

# Example: create db
createdb -O  <owner> -E 'UTF8' <db>
exit

# Test PostgreSQL connection by running a simple query
# Method 1: Run as postgres user directly
sudo -u postgres psql -c "SELECT 1"
# Method 2: Switch to postgres user and run query
sudo su - postgres -c "psql -c \"SELECT 1\""

# Execute commands as postgres
sudo su - postgres <<EOF
...
EOF
```
### Docker
```bash
docker run --name postgres -e POSTGRES_USER=postgres -e POSTGRES_PA
SSWORD=postgres -e POSTGRES_DB=todo_db -p 5432:5432 -d postgres:17
```

## Management
```bash
# List statuses of the installed clusters
sudo systemctl status 'postgresql*'
# or
sudo service postgresql status
# Restart postgresql service to ensure clean state
sudo systemctl restart postgresql
# Stop the specific PostgreSQL instance running version 10
# The '@10-main' specifies the version and cluster name
sudo systemctl stop postgresql@10-main
# Get a list of all postgres clusters
pg_lsclusters
# Create and start a new PostgreSQL cluster version 10 named 'main'
sudo pg_createcluster --start 10 main
# Stop and remove PostgreSQL cluster version 11 named 'main'
sudo pg_dropcluster --stop 11 main
# Forcefully terminate all postgres processes
sudo pkill -9 postgres
```

## Configuration

Possibly postgresql settings need to be updated

### `postgresql.conf`
```bash
cd /etc/postgresql/{version}/main/
sudo nano postgresql.conf

# add the line to the file configuring PostgreSQL service to listen on all network
listen_addresses = '*'
# Defines the network port to accept client connections
port = 5432
```

### `pg_bha.conf`
```bash
cd /etc/postgresql/{version}/main/
sudo nano pg_hba.conf

# add the following entry if not exist
# PostgreSQL will accept connections from all hosts on the network 0.0.0.0/0
host    all             all             0.0.0.0/0               scram-sha-256
# or
host    all             all             0.0.0.0/0               md5
# Side note: To allow X.X.X.X set 0.0.0.0/0, 192.X.X.X set 192.0.0.0/8, 192.168.X.X set 192.168.0.0/16, 192.168.1.X set 192.168.1.0/24, and only 192.168.1.2 set 192.168.1.2/32
```

Remember to restart PostgreSQL service after updates.

## Troubleshooting

### Cluster status is down
```bash
# If the cluster is down, its status shows 'down' in the list. For example
Ver Cluster Port Status Owner    Data directory              Log file
10  main    5432 down   postgres /var/lib/postgresql/10/main /var/log/postgresql/postgresql-10-main.log
# Then run the following commands
sudo chmod 700 -R /var/lib/postgresql/10/main
sudo -i -u postgres
/usr/lib/postgresql/10/bin/pg_ctl restart -D /var/lib/postgresql/10/main
# More configuartions
/usr/lib/postgresql/10/bin/pg_ctl restart \  # Restart PostgreSQL using pg_ctl
-D /var/lib/postgresql/10/main \            # Specify data directory
-l /var/log/postgresql/postgresql-10-main.log \  # Specify log file location
-s \                                        # Show progress messages
-o '-c config_file="/etc/postgresql/10/main/postgresql.conf"'  # Pass config file location
# Maybe restart the service
sudo systemctl restart postgresql
# Check the status again
pg_lsclusters
# If the output shows the cluster is online then it is ok
```

### psql: could not connect to server
    psql: could not connect to server: No such file or directory
    Is the server running locally and accepting
    connections on Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?
```bash
# make sure the localhost setting in /etc/hosts
127.0.0.1    localhost
```

### perl: warning: Setting locale failed
```bash
sudo locale-gen fi_FI.UTF-8
```

### Unknown user `postgres`
```bash
# Check if postgres user exists
id -u postgres >/dev/null 2>&1 || echo "postgres user not found"

# Add postgres user to sudo group if needed
sudo usermod -aG sudo postgres

# Verify postgres user's sudo privileges
sudo -l -U postgres

# Check user's group membership
groups postgres
```

## psql
```bash
# Switch to the postgres user
sudo su - postgres

# Check if database exists using PostgreSQL command line
# -t: Print only tuples (no headers or footers)
# -c: Execute single command then exit
# SELECT 1 returns 1 if database exists, nothing otherwise
# grep -q 1: Silently check if output contains 1 (database exists)
psql -tc "SELECT 1 FROM pg_database WHERE datname = 'dbname'" | grep -q 1

# Start the PostgreSQL interactive shell
psql
# Location: /usr/lib/postgresql/<version>/bin/psql

# Returns true if database exists, false otherwise
SELECT EXISTS (
    SELECT 1 FROM pg_database WHERE datname = 'db_name'
);

# Create role user
CREATE ROLE <role> WITH SUPERUSER LOGIN ENCRYPTED PASSWORD <pw>;
# Alter user's right
ALTER ROLE <role> WITH Superuser;
# Alter user password
ALTER USER username WITH PASSWORD 'newpass';
# Create database db for user role
CREATE DATABASE <db> WITH OWNER <role> ENCODING 'UTF8';

# Displays a list of all databases
\l

# list existing roles
\du

# Exit psql
\q

# Exit the postgres user shell
exit

# Use sshpass to securely connect to remote host and manipulate PostgreSQL dtabase
# Example shows how to drop PostgreSQL database if it exists
# -p: provide password non-interactively
# -oStrictHostKeyChecking=no: automatically accept new host keys
# -t: force pseudo-terminal allocation
sshpass -p <pw> ssh -oStrictHostKeyChecking=no -t user@host 'cd / && echo pw | sudo -S -u postgres dropdb --if-exists db'
```

**Note:** When switching to the postgres user from root, prefer using `su - postgres` over `su postgres`. The `-` flag ensures you get a full login shell with the postgres user's complete environment, including the correct home directory and PATH settings. This is particularly important for PostgreSQL operations that rely on proper environment configuration. For more details, consult the manual page using `man su`.


## pgAdmin4
### Installation
```bash
# Add the pgAdmin4 repository
sudo curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add
sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list'

sudo apt update
sudo apt install pgadmin4

# Config pgadmin4
sudo /usr/pgadmin4/bin/setup-web.sh
# Follow the prompts to set up an email and password for the pgAdmin web interface.
# Start the pgAdmin Web Server
sudo /usr/pgadmin4/bin/pgadmin4-web
```
