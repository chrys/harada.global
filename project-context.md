# Harada Project Context

## Overview

- Django application for building and managing Harada method charts.
- Server-rendered templates with HTMX for modal interactions and partial updates.
- Authentication is handled through Django auth plus custom Clerk middleware in `config/clerk_middleware.py`.
- Primary apps are `accounts`, `charts`, `wizard`, and `matrix`.

## Runtime And Tooling

- Python environment: local `.venv` is present in the repo.
- Dependencies are defined in `requirements.txt`; there is no Node or frontend package manager in this workspace.
- Test runner is `pytest` with `DJANGO_SETTINGS_MODULE=config.settings` from `pytest.ini`.
- Default database is SQLite in development via `db.sqlite3`; production DB is configured through `dj_database_url`.

## Commands Agents Should Use

```bash
source .venv/bin/activate
python manage.py runserver
python manage.py showmigrations
python manage.py makemigrations <app_name>
python manage.py migrate
pytest Tests/unit/ -v
pytest Tests/unit/ -v --cov=accounts --cov=charts --cov=matrix --cov=wizard --cov-report=term-missing
gunicorn -c gunicorn_config.py
```

## Architecture Boundaries

### `accounts`
- Handles login, registration, and dashboard views.
- Integrates with Clerk-backed auth flow through middleware rather than a standalone auth service layer.

### `charts`
- Holds core domain models such as `HaradaChart`, `Pillar`, `Task`, and `TaskComment`.
- Treat changes here as core model changes and ask before altering schema or semantics.

### `wizard`
- Implements the multi-step chart creation flow.
- Supports unauthenticated progress by storing temporary chart data in the session, then migrating to database records after authentication.
- The session-backed flow is a project-specific behavior; do not replace it casually.

### `matrix`
- Renders the 9x9 Harada matrix and handles task and pillar editing.
- Keep deterministic placement logic in `matrix/services.py`; that file is the source of truth for grid geometry.
- HTMX modal endpoints and partial-template responses live in `matrix/views.py`.

## Conventions That Matter Here

- Prefer function-based views with Django decorators. Match the surrounding style before introducing CBVs or forms.
- Keep business rules out of templates. Reusable grid or mapping logic belongs in services or model-adjacent code.
- Preserve HTMX response patterns already used in the repo:
  - render a partial template for modal content
  - return an empty `HttpResponse("")` when the client should just close a modal
  - use `HX-Refresh` or OOB swaps only when consistent with existing endpoints
- Use `get_object_or_404`, `select_related`, and `prefetch_related` rather than repeated ad-hoc queries.
- Follow existing naming and style: PEP 8, double quotes, f-strings, explicit variable names.
- Add or update NumPy-style docstrings for modified Python functions when the function contains non-trivial logic.

## Testing Conventions

- Tests live under `Tests/unit/`, usually grouped by app.
- Shared fixtures live in `Tests/conftest.py`.
- For non-trivial changes, follow TDD: write or update a failing test first, then implement until green.
- When fixing regressions in `matrix` or `wizard`, add a targeted regression test close to the affected area.

## Important Files To Read Before Editing

- `config/settings.py`: environment expectations, middleware, and security settings.
- `config/clerk_middleware.py`: custom auth synchronization and Clerk-specific behavior.
- `matrix/services.py`: deterministic matrix grid mapping.
- `matrix/views.py`: HTMX endpoint patterns and queryset prefetching.
- `wizard/views.py`: session-backed draft flow and chart migration logic.
- `Tests/conftest.py`: fixture conventions.
- `conductor/workflow.md`: repo workflow expectations and quality gates.

## Environment Expectations

Settings require these environment variables at minimum:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CLERK_SECRET_KEY`
- `CLERK_PUBLISHABLE_KEY`

If environment configuration looks incomplete, inspect `config/settings.py` rather than assuming `.env.example` is authoritative.

## Ask First

- Before modifying schema or creating migrations that touch production data.
- Before changing core models in `charts/models.py`.
- Before adding dependencies to `requirements.txt`.
- Before changing auth flow, Clerk behavior, or public URLs.
- Before introducing new frontend libraries or replacing HTMX/server-rendered patterns.

## Known Pitfalls

- Existing guidance in `.github/copilot-instructions.md` referenced `project-context.md`; this file is now that source of truth.
- `conductor/workflow.md` contains generic examples such as `--cov=app`; adapt coverage commands to actual apps in this repo.
- Session-backed wizard charts and authenticated database charts follow different code paths. Check both when changing wizard behavior.
- Matrix layout constants are easy to break accidentally; treat coordinate changes as high-risk and cover them with tests.
