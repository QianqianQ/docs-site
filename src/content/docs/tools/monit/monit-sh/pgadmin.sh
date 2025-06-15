#!/bin/bash

# this sh file assumes that pgadmin is installed globally without virtual env.
# uses nohup to run in background and outputs log to /etc/monit/log directory
# make sure to make this file executeable -> chmod +x and create directory logs

process=$1
case $process in
    start)
        echo "Starting pgadmin in port 5050"
        nohup /usr/bin/python3 /usr/local/lib/python3.6/dist-packages/pgadmin4/pgAdmin4.py  > /etc/monit/logs/pgadmin.log 2>&1 &
        ;;

    stop)
        pkill -f pgadmin
        ;;

    *)
        echo "INVALID OPTION"
        ;;
esac
