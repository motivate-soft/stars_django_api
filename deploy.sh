#!/bin/sh
sudo git pull origin master
sudo pip3 install -r requirements.txt
sudo systemctl restart nginx
sudo systemctl restart gunicorn
sudo systemctl restart gunicorn.socket