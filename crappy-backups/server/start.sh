#!/bin/bash
gunicorn server:app --bind 0.0.0.0:5001 --worker-class gthread --threads 4 --timeout 28800 --workers 1 
# download better finish in 8 hours or shits fucked
