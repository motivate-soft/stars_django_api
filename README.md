
<h1 align="center">starsofboston api👋</h1>


> vacation rental booking and management system

### 🏠 [starsofboston.com](https://www.starsofboston.com)


### ✨ [Demo](http://stars-website-react-2.ue.r.appspot.com/)


## Technologies
```
django/django-rest-framework
```

## Run development server
#### Create vitualenv
```
python -m venv venv
cd venv
cd Scripts
cd activate
```
#### Install dependencies and migrate
```
python manage.py -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py loaddata fixtures/db.json                  # seed database if needed
python manage.py runserver

```
Server starts at [localhost:8000](http://localhost:8000)
## Prepare for production

### Create .env in root dir
```
SECRET_KEY=
DEBUG=False
BOOKERVILLE_API_KEY=
SENDGRID_API_KEY=
DB_HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
```