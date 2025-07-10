#!/bin/sh

#git pull
cd src/
#pip install -r requirements.txt
python api/manage.py migrate
python api/manage.py runserver 0.0.0.0:8000