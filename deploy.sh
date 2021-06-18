#!/bin/sh
sudo git pull origin master
source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
sudo systemctl restart gunicorn.socket
sudo systemctl restart gunicorn
sudo systemctl restart nginx