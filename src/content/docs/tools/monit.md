---
title: Monit
description: Monit.
---
Monit is a small Open Source utility for managing and monitoring Unix systems.
Monit conducts automatic maintenance and repair and can execute meaningful
causal actions in error situations.

## Installation
```bash
# update or upgrade system
sudo apt-get update && sudo apt-get upgrade

# install monit
sudo apt install monit

# enable/start monit Daemon
sudo monit

# check status of monit
sudo systemctl status monit

# configure monit settings
sudo nano /etc/monit/monitrc
```

    For maintenance do not add process checks inside `monitrc`, only append
    monit related settings etc. daemon cycle, emails etc. Also keep backup before
    modifying the original.

## Configuration
1. Add new configurations inside `conf.d`
    some important notes, check section - [Monitrc configuration](#monitrc-configuration) for useful monitrc configuration tips

2. Restart the monit daemon
    ```bash
    sudo service monit restart
    ```

3. Make sure monit start when reboot
    ```bash
    sudo systemctl enable monit
    # or
    sudo update-rc.d monit enable
    ```

4. visit web interface - `<url>:2812`

## Directory structure for monit at - /etc/monit/ ##
```
├── conf-available        --------------------------->> Available samples
│   ├── acpid
│   ├── apache2
│   ├── at
│   ├── cron
│   ├── mdadm
│   ├── memcached
│   ├── mysql
│   ├── nginx
│   ├── openntpd
│   ├── openssh-server
│   ├── pdns-recursor
│   ├── postfix
│   ├── rsyslog
│   ├── smartmontools
│   └── snmpd
├── conf-enabled
├── conf.d                -------------------------->> Custom config files
│   ├── apache2
│   ├── jenkins
│   ├── pgadmin
│   └── postgres
├── logs                  --------------------------->> Custom directory to store logs - eg. used by sh/pgadmin.sh
├── monitrc               --------------------------->> Monit main config file
├── pgadmin
├── sh                    --------------------------->> Custom shell script directory to store sh files to run/stop/restart services via shell
│   ├── pgadmin.sh
│   └── postgres.sh
└── templates
    ├── rootbin
    ├── rootrc
    └── rootstrict
```
    Logs and sh directries are custom directories created after installation.
    The main idea is not all servers run the same commands to start or stop the
    software if they have different versions of software or OS. Therefore
    if shell script is required to run a software then those are placed inside sh
    directory and called from configuration inside conf.d directory, similary log
    directory is used to store the those script's logs which it generates. Also it's not
    necessary that logs or sh files should be inside `/etc/monit/` dir. It's optional.

Make sure custom directories has permission 600
```bash
chmod 600 <file_or_dir>
```

## Monitrc configuration

Edit `/etc/monit/monitrc`
```bash
# make 5 min interval for daemon so that server load is not high
set daemon 300

# Allow 2812 port to allow web interface from browser and disable only localhost if necessary
set httpd port 2812
    # use address localhost   # only accept connection from localhost
    # allow localhost         # allow localhost to connect to the server and
    allow user:pw      # require user 'admin' with password 'monit'

# smtp setting for email alerts
set mailserver mail_address   # primary mailserver`

# custom directory for configurations can be added
include /etc/monit/conf.d/*
```

`monit` directory contains some configs.