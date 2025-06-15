---
title: Sphinx
description: Sphinx.
---
`sphinx` directory contains the Sphinx documentation setup for the project, including build scripts and deployment automation. The documentation is built using Sphinx and deployed to remote servers using Ansible. The deployment process includes fetching static assets, building the documentation, and configuring Apache2 on the target server.

Key features:
- Automated deployment via `deploy_docs.sh` script
- Ansible playbook for building and deploying documentation
- Apache2 configuration template for serving docs
- Version-controlled documentation source in RST format

## Folder structure
<pre>
.
├── build/			    # Output directory for compiled documentation (HTML, PDF, etc.).
├── deploy_docs.sh      # Bash script for automating steps of selecting deployment server,
fetching required static files, building and deploying wiki.
├── deploy.yml          # Ansible playbook for building and deploying wiki.
├── inventory.ini       # Ansible inventory file with hosts and vars definitions.
├── make.bat            # Sphinx build script for Windows.
├── Makefile            # Sphinx build script for Linux/macOS.
├── README.md
├── secret.enc          # Encrypted secrets file (managed by ansible-vault).
├── source/             # Source directory for wiki built by Sphinx.
│	├── xxx.rst   # Cloud native track version history. Add new entry to update releases.
│	├── conf.py                  # The main Sphinx configuration file.
Defines project info, extensions, and theme settings.
If app version is updated, the var `release` needs to be updated as well.
│	├── index.rst                # The entry point for the documentation (home page).
│	├── _static/                 # Stores custom CSS, JS, or images for styling.
│	├── _templates/              # Custom templates to override default Sphinx layouts.
└── docs_apache2.conf.j2         # Apache2 wiki site configuration.
</pre>

## Build
```bash
wget --quiet --directory-prefix source/_static/images/  link/to/images.tar
tar -xf source/_static/images/images.tar -C source/_static/images/

# Make any changes as needed, then build
make html
```