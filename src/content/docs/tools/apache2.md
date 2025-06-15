---
title: Apache2
description: Apache2 Commands.
---

```bash
# Display a list of all modules that are currently loaded into the Apache HTTP Server.
apachectl -M

# Check all the enabled Apache modules
ls /etc/apache2/mods-enabled

# Check all the available Apache modules
ls /etc/apache2/mods-available

# Enable module
sudo a2enmod <module_name>
# Enable the mod_rewrite module, which is a powerful tool for rewriting URLs
sudo a2enmod rewrite

# Disable module
sudo a2dismod <module_name>

# Restart Apache
sudo systemctl restart apache2
```