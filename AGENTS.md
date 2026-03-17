# Harada Agent Guide

Read `project-context.md` first. It is the shared source of truth for this repo.

## Scope

This workspace is a Django application for the Harada method. Use Django, pytest, HTMX, and the existing server-rendered template patterns already in the codebase. There is no Node build chain in this repo.

## Default Workflow

1. Read `project-context.md` and inspect the files you plan to edit.
2. For non-trivial changes, write or update a failing pytest first.
3. Implement the smallest change that satisfies the requirement.
4. Run targeted validation, then broader tests if warranted.
5. Report risks, especially around migrations, auth, and queryset behavior.

## Commands

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

## Repo Conventions

- Prefer function-based Django views and existing decorator-based access control.
- Preserve HTMX endpoint patterns in `matrix/views.py`.
- Keep matrix geometry logic in `matrix/services.py`.
- Preserve the session-backed wizard flow in `wizard/views.py` unless the task explicitly changes it.
- Use `get_object_or_404`, `select_related`, and `prefetch_related` to avoid ad-hoc query sprawl.
- Follow PEP 8, double quotes, f-strings, and explicit names.
- Add type hints and NumPy-style docstrings for non-trivial Python functions you create or materially change.

## Ask First

- Schema changes or production-impacting migrations.
- Core model changes in `charts/models.py`.
- New dependencies in `requirements.txt`.
- Auth or Clerk flow changes.
- Public URL changes.
- New frontend frameworks or architecture changes.

## High-Risk Areas

- `config/clerk_middleware.py`: auth behavior and security implications.
- `wizard/views.py`: temporary session chart flow versus authenticated DB-backed flow.
- `matrix/services.py`: deterministic coordinate mapping for the 9x9 grid.

## Good Files To Study First

- `project-context.md`
- `config/settings.py`
- `matrix/views.py`
- `matrix/services.py`
- `wizard/views.py`
- `Tests/conftest.py`
- `conductor/workflow.md`

## Response Style

- Be direct and implementation-focused.
- State assumptions when the request is ambiguous.
- Do not do unrelated cleanup.
- If a refactor leaves dead code behind, list it and ask before removing it.
