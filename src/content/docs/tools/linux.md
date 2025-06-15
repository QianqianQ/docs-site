---
title: Linux
description: Linux.
---

## System config and info
```bash
# Check username
echo $USER

# View system users and their information
less /etc/passwd
cat /etc/passwd | less

# Check Linux distribution and version
cat /etc/os-release

# Check if a package is installed
dpkg -l | grep <package_name>

# List all installed package-related packages with their installation status
# --get-selections: Shows package names and their install/remove/purge status
dpkg --get-selections | grep <package_name>

# List all APT repository configuration files with details
# -a: Show hidden files (those starting with .)
# -l: Use long listing format showing permissions, ownership, size, and modification time
ls -al /etc/apt/sources.list.d/
```

## `~/.bashrc` configuration
```bash
# Add environment variable example: Add ChromeDriver to PATH for browser automation
export PATH=$PATH:/path/to/chromedriver-linux64/
# Alias example: Quick navigation and virtualenv activation for app
alias app='cd /app && source ~/virtualenvs/app/bin/activate'
# Set default text editor to nano for command line tools
export EDITOR=nano
# Set default visual editor to nano for GUI applications
export VISUAL=nano
```

## Service management
```bash
# Restart service
# service: legacy init system command
# systemctl: modern systemd command
sudo service <service_name> restart
sudo systemctl restart <service_name>

# Increase inotify watcher limit to prevent "too many open files" errors
# - Adds fs.inotify.max_user_watches=524288 to /etc/sysctl.conf
# - Reloads sysctl settings to apply changes immediately
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
```

## Process handling
```bash
# Check running PostgreSQL processes
# -C option selects processes by command name
ps -C postgres

# List processes with:
# -e: all processes
# -o: custom output format showing:
#   pid: process ID
#   comm: command name (truncated to 15 chars)
#   %cpu: CPU usage percentage
# --sort=-%cpu: sort by CPU usage in descending order
ps -eo pid,comm,%cpu --sort=-%cpu

# List processes using port 5432 (PostgreSQL default port)
# lsof (list open files) shows processes using files/ports
# -i: select internet connections
# :${port_number}: filter for specific port
sudo lsof -i :5432

# Forcefully terminate process with given PID (use with caution as it doesn't allow cleanup)
# -9 sends SIGKILL signal which forcefully terminates the process
sudo kill -9 pid

# Kill process running on a specific port
# -t: show only process IDs
sudo kill $(sudo lsof -t -i:${port_number})
# Alternative: kill process forcefully if needed
sudo kill -9 $(sudo lsof -t -i:${port_number})
```

## Networking

The `.netrc` file is used to store login credentials for remote servers, allowing for automated authentication when using tools like FTP or curl.
```bash
$ nano ~/.netrc  # Open the .netrc file in the nano text editor
# Add credentials for automated login
machine example.com  # Specify the machine name
  login myusername  # username for authentication
  password mypassword  # password for authentication

$ chmod 600 ~/.netrc  # Set file permissions to read/write for the user only
```

```bash
# check public addresses
# https://whatismyipaddress.com/
curl ifconfig.me

# private addresses
ipconfig
# IPv4 Address

# Check DNS servers
ipconfig /all
# DNS Servers line

# What is the IP address of your router (gateway)? How do you "ping" it?
ipconfig  # Default Gateway
ping <default_gateway_ip>

# Use IPv4 only
ping <ip> -4

# How many hops does it take to reach Google's search engine? Where do most delays occur?
tracert google.com

# What IP address does "www.google.com" resolve to? Did it return more than one?
nslookup google.com
# PS
Resolve-DnsName www.google.com

# Ubuntu
# public
curl ifconfig.me

# private
ip a  # ip address
hostname -I
# require installation
ipconfig

# DNS server
resolvectl status
cat /etc/resolv.conf

# gateway
ip route | grep default
ping

# How many hops does it take to reach Google's search engine? Where do most delays occur?
# traceroute needs to be installed
traceroute google.com
```

## Secure Shell Protocol (SSH)

For a new machine, create an SSH key
```bash
# Generate a new SSH key with 4096 bits
ssh-keygen -t rsa -b 4096

# Check SSH public key
cat ~/.ssh/id_rsa.pub

# Copy the SSH key to the remote host for authentication
ssh-copy-id -i ~/.ssh/id_rsa.pub <remoteuser>@<remoteserver>

# Bypass host key verification
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null user@host
```

The SSH config file allows you to define shortcuts for SSH connections.
```bash
$ cat ~/.ssh/config
Host name                # Define a shortcut name for the SSH connection
  User user_name         # Specify the username
  Hostname ip_address    # Provide the IP address or hostname of the remote server
  Port port              # Specify the port number (default is 22)

$ ssh name
```
### sshpass
```bash
# Installation
sudo apt install sshpass
```

## File handling
```bash
# Download a file
wget <file_url>

# Remove file
rm <file>

# Compress the directory into a tar.gz archive
# -c: create new archive
# -z: compress using gzip
# -v: verbose (show progress)
# -f: specify output filename
tar -czvf <tar_name>.tar.gz dir/

# Extract a tar.gz file
# -x: extract files
# -v: verbose (show progress)
# -z: uncompress gzip file
# -f: specify filename
tar -xvzf <tar_file>

# Copy file to remote server
scp <local_file_path> server:<remote_server_path>
```

## Python
```bash
# Install python with specific version 3.11
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
sudo apt install python3.11-venv
python3.11 -m venv .venv
```

## mediawiki

### Setup
```bash
# Copy MediaWiki archive to remote host
scp mediawiki-1.40.0.tar.gz user@host:/home/user

# Move and extract MediaWiki files
ssh user@host "
    sudo mv /home/user/mediawiki-1.40.0.tar.gz /var/www/ &&
    sudo tar -xzvf /var/www/mediawiki-1.40.0.tar.gz -C /var/www/ &&
    sudo mv /var/www/mediawiki-1.40.0 /var/www/mediawiki
"

# Configure MediaWiki
ssh user@host "
    sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/mediawiki.conf &&
    sudo nano /var/www/mediawiki/LocalSettings.php  # Update database settings
"

# Create MediaWiki database in PostgreSQL
ssh user@host "
    sudo -u postgres psql -c \"CREATE DATABASE mediawiki WITH OWNER mediawiki_user ENCODING 'UTF8';\"
"

# Run MediaWiki installation
ssh user@host "
    cd /var/www/mediawiki/maintenance &&
    php install.php --dbname mediawiki --dbuser mediawiki_user --dbpass password --pass localhero --scriptpath / --server http://example.com mediawiki admin_user  # admin_user is the username for the initial administrator account
"
```

## Ubuntu 18 to 22 upgrade
```bash
# php

php -version

# Configure PHP

# Check all the enabled Apache modules
ls /etc/apache2/mods-enabled
# There will be php7.x.conf and php7.x.load files for php7.x module, and it needs to be disabled
sudo a2dismod php7.x

# Check all the available Apache modules
ls /etc/apache2/mods-available
# There will be php8.x.conf and php8.x.load files for php8.x module, and it needs to be enabled
sudo a2enmod php8.X

# Restart apache2 service
sudo systemctl restart apache2

# Display a list of all modules that are currently loaded into the Apache HTTP Server.
apachectl -M


# PostgreSQL
# Check PostgreSQL server version
sudo -u postgres psql -c 'SELECT version();'

# Check PostgreSQL client version
psql -V

# It is possible server and client have different versions. It is recommended but not mandatory to have the same version

# List all installed packages related to PostgreSQL
dpkg --get-selections | grep postgres

# List all the running PostgreSQL clusters
pg_lsclusters

# If there are multiple clusters, the following configuration needs to be checked and updated if needed

# For the PostgreSQL with the server version showed from the first command
# in /etc/postgresql/<major-version-number>/main/postgresql.conf
# Update the following config if needed. listen_addresses may be commented out, uncomment it
listen_addresses = '*'
port = 5432
# in /etc/postgresql/<major-version-number>/main/pg_hba.conf
# Add the following config if not exists
host    all             all             0.0.0.0/0               scram-sha-256
# Or
host   all              all             0.0.0.0/0              md5
```