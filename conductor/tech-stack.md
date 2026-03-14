# Technology Stack - HaradaFlow

## Core Technologies
- **Language:** [Python](https://www.python.org/)
- **Backend Framework:** [Django 4.2+](https://www.djangoproject.com/)
- **Frontend Interactivity:** [HTMX](https://htmx.org/) (specifically `django-htmx`)
- **Styling:** [Tailwind CSS](https://tailwindcss.com/)
- **Database:** [PostgreSQL](https://www.postgresql.org/)

## Infrastructure & Deployment
- **Web Server:** [Gunicorn](https://gunicorn.org/)
- **Database Connector:** `psycopg2-binary`
- **Config Management:** `dj-database-url`, `python-dotenv`
- **Authentication:** [Clerk](https://clerk.com/) (integrated via middleware and templates)
- **Deployment Platform:** Render (inferred)

## Development & Testing
- **Testing Framework:** [Pytest](https://pytest.org/) (with `pytest-django`, `pytest-factoryboy`)
- **JWT Handling:** `PyJWT`
- **Code Linting:** (Standard Python/Django best practices)
