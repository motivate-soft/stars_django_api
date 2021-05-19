#!/bin/sh
sudo git pull origin master
sudo source venv/bin/activate
pip3 install -r requirements.txt
sudo systemctl restart gunicorn.socket
sudo systemctl restart gunicorn
sudo systemctl restart nginx