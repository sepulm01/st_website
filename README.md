# st_website


## Demonizar Celery beat

Editar el archivo de configuración

```
sudo nano /etc/conf.d/celery
```

```
# Name of nodes to start
# here we have a single node
CELERYD_NODES="w1"
# or we could have three nodes:
#CELERYD_NODES="w1 w2 w3"

# Absolute or relative path to the 'celery' command:
CELERY_BIN="/root/env/bin/celery" 

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="mysite"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# How to call manage.py
CELERYD_MULTI="multi"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=8"

# - %n will be replaced with the first part of the nodename.
# - %I will be replaced with the current child process index
#   and is important when using the prefork pool to avoid race conditions.
CELERYD_PID_FILE="/var/run/celery/%n.pid"
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_LOG_LEVEL="INFO"

# you may wish to add these options for Celery Beat
CELERYBEAT_PID_FILE="/var/run/celery/beat.pid"
CELERYBEAT_LOG_FILE="/var/log/celery/beat.log"
```

Luego editar los siguientes archivos de servicios de systemd, correspondientes al worker y el otro a beat.


archivo para worker
```
sudo nano /etc/systemd/system/celery.service
```

```
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=root
Group=root
EnvironmentFile=/etc/conf.d/celery
WorkingDirectory=/var/www/st_website
RuntimeDirectory=celery
ExecStart=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi start $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --loglevel="${CELERYD_LOG_LEVEL}"'
ExecReload=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi restart $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
Restart=always

[Install]
WantedBy=multi-user.target
```

archivo para beat
sudo nano /etc/systemd/system/celerybeat.service

```
[Unit]
Description=Celery Beat Scheduler Service
After=network.target

[Service]
Type=simple
User=root
Group=root
EnvironmentFile=/etc/conf.d/celery
WorkingDirectory=/var/www/st_website
RuntimeDirectory=celery
ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} beat  \
    --pidfile=${CELERYBEAT_PID_FILE} \
    --logfile=${CELERYBEAT_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL}'
Restart=always

[Install]
WantedBy=multi-user.target
```

Crear los directorios:

```
sudo mkdir /var/log/celery /var/run/celery
sudo chown reclamosegurochile:reclamosegurochile /var/log/celery /var/run/celery 
```
BUG: hay problemas con el directorio /var/run/celery al hacer un reboot, así que hay que crearlo nuevamente y darle los privilegios

luego habilitar los servicios:

```
sudo systemctl daemon-reload
sudo systemctl enable celery
sudo systemctl enable celerybeat
sudo systemctl start celery
sudo systemctl start celerybeat

cat /var/log/celery/beat.log

cat /var/log/celery/w1.log
```