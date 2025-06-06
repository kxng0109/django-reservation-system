# Django Reservation System

A simple reservation/booking system built with Django—practice for CRUD operations, forms, validation, and templating, with flexible database and deployment configuration.

---

## Table of Contents

1. [Features](#features)  
2. [Tech Stack](#tech-stack)  
3. [Requirements](#requirements)  
4. [Project Structure](#project-structure)  
5. [Setup (Local Development)](#setup-local-development)  
6. [Environment Variables](#environment-variables)  
7. [Database Configuration & Fallbacks](#database-configuration--fallbacks) 
8. [Deployment (Generic)](#deployment-generic)  
9. [Usage](#usage)  
10. [License](#license)  

---

## Features

- Public reservation form (first name, last name, date, party size, notes)  
- `date` validation prevents today or past-date bookings  
- Staff‐only pages (list, detail, edit, delete) protected by `is_staff`  
- Plain CSS styling for forms, tables, alerts, and navigation  
- Full CRUD: create, read, update, and delete reservations  
- Flexible database setup: Neon Postgres, Docker Compose Postgres, or SQLite fallback  
- Production‐ready environment‐variable and static‐file configuration

---

## Tech Stack

- **Python 3.13+**  
- **Django 4.x**  
- **Gunicorn** (WSGI server)  
- **WhiteNoise** (static file serving)  
- **PostgreSQL** (Neon, Docker Compose, or any `DATABASE_URL`)  
- **SQLite** (optional fallback)  
- **Plain CSS** (no CSS framework)  
- **python-dotenv** (load `.env` in local dev)  
- **dj-database-url** (parse database URLs)

---

## Requirements

- Python 3.13 or higher  
- `pip` (package manager)  
- Git  
- (Optional) Docker & Docker Compose  
- (Optional) pyenv (if you use `.python-version`)  
- (Optional) A hosting environment that supports Python/WGS

---

## Project Structure

```

booking-system/
├── config/                          # Django project settings
│   ├── **init**.py
│   ├── asgi.py
│   ├── settings.py                  # Configured for multi-environment
│   ├── urls.py
│   └── wsgi.py
│
├── reservations/                    # Django app
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html
│   │   ├── make\_reservation.html
│   │   ├── reservation\_delete\_confirmation.html
│   │   ├── reservation\_detail.html
│   │   ├── reservation\_form.html
│   │   ├── reservation\_list.html
│   │   └── reservation\_success.html
│   ├── **init**.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── static/                          # Project-level static assets
│   └── reservations/
│       └── css/
│           └── styles.css
│
├── venv/                            # Virtual environment (ignored by Git)
│
├── .env                             # Local environment variables (gitignored)
├── .python-version                  # (Optional, for pyenv)
├── runtime.txt                      # (For Heroku and other hosts)
├── Procfile                         # (For Heroku, Gunicorn command)
├── docker-compose.yaml              # (Optional, Docker Compose config)
├── manage.py
├── requirements.txt
└── .gitignore

````

---

## Setup (Local Development)

1. **Clone the repository**  
   ```bash
   git clone https://github.com/kxng0109/django-reservation-system.git
   cd django-reservation-system
````

2. **(Optional) Install pyenv and create `.python-version`**
   If you use `pyenv`, run:

   ```bash
   pyenv install 3.13.3
   pyenv local 3.13.3
   ```

   This will create a `.python-version` file with `3.13.3`.

3. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate       # macOS/Linux
   venv\Scripts\Activate.ps1      # Windows PowerShell
   ```

4. **Install Python dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Create a `.env` file** (for local development)
   At the project root, create a file named `.env` with contents like:

   ```dotenv
   DJANGO_SECRET_KEY="your-local-secret-key"
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   # Optional: use a serverless database, for example Neon or other Postgres in local development
   # DATABASE_URL="postgresql://neon_user:neon_pass@db.neon.com:5432/neon_db?sslmode=require"
   # if you're using a docker postgresql server container
   # POSTGRES_USER="user"
   # POSTGRES_PASSWORD="pass"
   # POSTGRES_DB="db"
   ```

6. **Run Docker Compose (Optional for Postgres)**
   If you want to use the included Docker Compose Postgres service:

   ```bash
   docker-compose up -d
   ```

   This will spin up a Postgres container on `localhost:5432` with credentials `user:pass`, database `db`. Django will pick it up automatically via our default URL.

7. **Apply migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

9. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   * Visit `http://127.0.0.1:8000/app/reserve/` for the public reservation form.
   * Visit `http://127.0.0.1:8000/admin/` to log in as staff.

---

## Environment Variables

Your project uses environment variables (loaded by `python-dotenv`) to configure secrets and production settings. Below are the most important variables:

```
DJANGO_SECRET_KEY="your-secret-string"  
DJANGO_DEBUG=False           # or 'True' in local development, make sure it is False for production
DJANGO_ALLOWED_HOSTS="domain1.com,domain2.com"  
DATABASE_URL="postgresql://user:pass@host:port/db?sslmode=require" 
POSTGRES_USER="user"
POSTGRES_PASSWORD="pass"
POSTGRES_DB="db"
```

* **`DJANGO_SECRET_KEY`**: Must be a strong random string in production.
* **`DJANGO_DEBUG`**: Set to `False` in production; `'True'` only for local testing.
* **`DJANGO_ALLOWED_HOSTS`**: Comma-separated list of hostnames allowed by Django; e.g. `"localhost,127.0.0.1"` locally or `"myapp.herokuapp.com"` in production.
* **`DATABASE_URL`**: Optional—if provided, Django uses it. Format depends on your Postgres provider (Neon, Heroku, AWS, etc.). If unset, Django falls back to the Docker Compose default.
* You can set these in a `.env` file (for local dev) or in your hosting environment’s configuration (e.g. through the control panel, Docker secrets, or CI/CD pipeline).

---

## Database Configuration & Fallbacks

In `config/settings.py`, the `DATABASES` section is configured like this:

```python
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, conn_health_checks=True)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
```

**Priority order**:

1. **`DATABASE_URL`** in environment (e.g. Neon Postgres connection or a docker container).
2. **(Optional) Local SQLite**, if you uncomment the SQLite block.

---

**How to use**:

1. Build and start containers:

   ```bash
   docker-compose up --build
   ```
2. Visit `http://localhost:8000/reserve/` in your browser.
3. The Django app will automatically connect to the `db` Postgres container.
4. To stop containers:

   ```bash
   docker-compose down
   ```

---

## Deployment (Generic)

Below is a **generic, multi-platform** approach. Depending on your host, you may skip or modify certain steps.

### 1. Pin Python Version

* **`runtime.txt`** (for Heroku and some PaaS):
  At the project root, create `runtime.txt` containing:

  ```
  python-3.13.3
  ```
* **`.python-version`** (for pyenv/local dev – optional):
  At the project root, create `.python-version` containing:

  ```
  3.13.3
  ```

### 2. Ensure Production Dependencies

Confirm `requirements.txt` includes at least:

```
asgiref==3.8.1
dj-database-url==3.0.0
Django==5.2.1
psycopg2-binary==2.9.10
python-dotenv==1.1.0
sqlparse==0.5.3
typing_extensions==4.14.0
tzdata==2025.2
whitenoise==6.9.0
```

### 3. Configure Static Files & WhiteNoise

In `config/settings.py`, ensure you have:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ... other middleware ...
]

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_ROOT = BASE_DIR/"staticfiles"

# To add caching and compression support from whitenoise
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    }
}
```

Run:

```bash
python manage.py collectstatic --noinput
```

to gather static files into `staticfiles/`.

### 4. Set Environment Variables on Your Host

Common variables:

```
DJANGO_SECRET_KEY="a-long-random-secret"
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS="mydomain.com,www.mydomain.com"
DATABASE_URL="postgresql://user:pass@neon-host:5432/neon_db?sslmode=require"
```

Set them via any platform you wish. 

### 5. Run Migrations & Start WSGI Server

On your production host, after pulling or building the code:

```bash
python manage.py migrate
# Optionally create a superuser:
python manage.py createsuperuser
# Start Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

If you’re behind Nginx, configure it to proxy to Gunicorn (e.g., `proxy_pass http://127.0.0.1:8000;`).

### 6. Verify and Monitor

* Visit your domain (e.g., `https://mydomain.com/app/reserve/`).
* Ensure static files load (CSS, images).
* Check logs (Heroku: `heroku logs --tail`; Linux: `journalctl -u myapp.service`).

---

## Usage

* **Public Form**:
  Visit `/app/reserve/` to create a new reservation.

* **Staff Pages** (requires staff login via Admin):

  * `/app/reservations/list/` → List all reservations
  * `/app/reservations/<pk>/` → View reservation details
  * `/app/reservations/<pk>/edit/` → Edit a reservation
  * `/app/reservations/<pk>/delete/` → Delete (cancel) a reservation

Manage staff permissions via the Django Admin (`/admin/`).

---

## License

This project is released under the MIT License. Feel free to use, modify, and distribute as you see fit.

---
