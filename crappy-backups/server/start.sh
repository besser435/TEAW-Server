#!/bin/bash
#gunicorn --workers 2 --bind 0.0.0.0:5001 --name teaw_backup_gunicorn server:app
gunicorn server:app --bind 0.0.0.0:5001 --worker-class gthread --threads 4 --timeout 3600 --workers 1 
# download better finish in 3600 seconds or shits fucked
