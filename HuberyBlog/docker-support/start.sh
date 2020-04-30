#!/bin/bash
cd /HuberBlog
mkdir -p /var/log/celery/
mkdir -p /var/run/celery
celery multi start w1 -A HuberyBlog -l info --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log
uwsgi --ini uwsgi.ini
nginx
