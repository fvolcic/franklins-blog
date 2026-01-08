# Franklin's Personal Website

A personal website and blog built with Django. Features markdown rendering for blog posts, an admin interface for content management, and page view analytics.

## Features

**Blog**

Posts are written in Markdown and rendered with syntax highlighting, tables, and table of contents support. The homepage redirects to an About Me page, with a separate blog section for all posts.

**Image Uploads**

Images can be uploaded through the Django admin. Each image displays a copyable Markdown snippet for easy embedding in posts.

**Analytics**

Page views are tracked individually with referrer URL, country (via IP geolocation), and timestamps. The admin includes a dashboard with charts showing views over time, top countries, popular posts, and referrers.

## Stack

Django 6.0, SQLite, Gunicorn, Nginx, Let's Encrypt SSL

## Local Development

```
python3 -m venv venv
source venv/bin/activate
pip install django markdown gunicorn Pillow
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Deployment

The site runs on Ubuntu with Gunicorn as the WSGI server and Nginx as a reverse proxy. Static files are served from `/staticfiles/` and media uploads from `/media/`.

Collect static files before deploying:

```
python manage.py collectstatic
```

Restart the service after changes:

```
sudo systemctl restart gunicorn
```
