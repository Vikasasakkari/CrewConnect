# CrewConnect

CrewConnect is a Django employee and HR management application.

## GitHub

GitHub stores and versions this project's source code. GitHub Pages only hosts
static websites; it cannot run this Django application, its database, or its
login and HR features. A live Django site needs a server that runs Python and
provides a database.

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
