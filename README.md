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
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and set your local database credentials.
   `.env` is ignored by Git. Set `SECRET_KEY` to a private random value.
3. Run the database migrations and start Django:

   ```powershell
   python manage.py migrate
   python manage.py runserver
   ```

## Hosted MySQL

Vercel cannot connect to MySQL running on your computer. Create a hosted MySQL
database with a provider that allows connections from Vercel, then add its
connection details to the Vercel project's Production environment variables.
Set `DATABASE_URL` to the provider's full MySQL connection URL, for example
`mysql://USER:PASSWORD@HOST:PORT/DATABASE`. URL-encode special characters in
the username and password. Keep credentials private. Production MySQL
connections use TLS and verify the server certificate and hostname.

After adding the database URL, redeploy so Vercel applies the variable. Pull
the Production environment locally and run the migrations with:

```powershell
vercel env pull .env.production.local --environment=production
dotenv -f .env.production.local run -- python manage.py migrate
```
