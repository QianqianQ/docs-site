---
title: Ansible
description: Ansible.
---

## How to run
```bash
ansible-playbook <yml_name>.yml -i hosts --ask-become-pass -u <user> --ask-vault-pass --extra-vars "var_name='value'"
```

## `sample-project` directory structure
The `sample-project` Ansible directory contains sample configuration and deployment scripts for setting up a web application environment. The main components include:

- **playbook.yml**: Main playbook that orchestrates deployment tasks across different hosts
- **hosts**: Inventory file defining target hosts
- **roles/web**: Contains tasks, templates, and configurations for web server setup
  - **templates/**: Jinja2 templates for Apache configuration and Django environment settings
  - **tasks/main.yml**: Defines the sequence of operations for web server configuration

Key features include:
- Apache web server configuration
- Django environment setup
- PostgreSQL database creation
- Ubuntu 22.04 specific package installation

## ansible-vault
```bash
# Encrypt existing file
# It will prompt for new password and confirmation
# Once the password is set it could be used for encrypting/decrypting the encrypted file
ansible-vault encrypt ${filename}

# View encrypted file with commandline vault-password
ansible-vault view ${encrypted-file-name} --ask-vault-pass

# Edit encrypted file with commandline vault-password
ansible-vault edit ${encrypted-file-name} --ask-vault-pass
```
