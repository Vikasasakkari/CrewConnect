# CrewConnect

CrewConnect is a Django employee and HR management application.

## GitHub

GitHub stores and versions this project's source code. GitHub Pages only hosts
static websites; it cannot run this Django application, its database, or its
login and HR features. A live Django site needs a server that runs Python and
provides a database.

When running on Vercel, the deployment's Vercel hostnames are added to
Django's allowed hosts automatically. If you attach a custom domain, add its
hostname (without `https://`) to the `ALLOWED_HOSTS` environment variable.

## Local development

1. Create and activate a virtual environment, then install the dependencies:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt -r requirements-mysql.txt
   ```

2. The extra `requirements-mysql.txt` installs the native MySQL driver needed
   for local MySQL development. For PostgreSQL-only environments, install just
   `requirements.txt`. Copy `.env.example` to `.env` and set your local
   database credentials. `.env` is ignored by Git. Set `SECRET_KEY` to a
   private random value.
3. Run the database migrations and start Django:

   ```powershell
   python manage.py migrate
   python manage.py runserver
   ```
