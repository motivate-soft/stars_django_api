
<h1 align="center">starsofboston api👋</h1>


> vacation rental booking and management system api

### 🏠 [starsofboston.com](https://www.starsofboston.com)


## Technologies
```
django/django-rest-framework
```

## Run development server
### Create vitualenv
##### windows
```
python -m venv venv
cd venv
cd Scripts
cd activate
```
#### Ubuntu
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Install dependencies and migrate
```
python manage.py -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py loaddata fixtures/db.json                  # seed database if needed
python manage.py runserver
```
Server starts at [localhost:8000](http://localhost:8000)

### Create .env in root dir
```
SECRET_KEY=
PRODUCTION=
BOOKERVILLE_API_KEY=
SENDGRID_API_KEY=
DB_HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
```

## Restart EC2 gunicorn service
connect to server with putty
```
cd /var/starsofboston/stars_django_api
sudo git pull origin master
sudo source venv/bin/activate
pip3 install -r requirements.txt
sudo systemctl restart gunicorn.socket
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```
OR run just one command
```
/bin/sh ./deploy.sh
```
