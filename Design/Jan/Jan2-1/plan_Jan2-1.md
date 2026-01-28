## Sprint Jan2-1 — Specs (MVP)

### Sprint Goal
Deliver the MVP HaradaFlow experience: a guided wizard to build a 64‑cell chart and a responsive 9x9 matrix view/edit screen aligned with the provided UI template.

### Scope
**In scope (MVP):**
- User authentication (register, login, logout).
- Create a Harada Chart via a 3‑step wizard.
- View/Edit a chart in an interactive 9x9 matrix with task detail modal.
- Persist charts, pillars, tasks, and progress.

**Out of scope (defer):**
- Export to PDF/CSV.
- Phase‑2 items (daily checklist, Soji reminder, color coding).

### UI/UX Alignment
- Base layout and visual language should mirror [Design/Jan/Jan2-1/template.html](Design/Jan/Jan2-1/template.html) and the sample image at Design/Jan/Jan2-1/template.png.
- Tailwind via CDN is acceptable for MVP; use the palette, fonts, and spacing already defined in the template.
- Provide dark mode support using the `dark` class, consistent with the template.

### Architecture & Apps
**Django apps:**
- `accounts`: auth, profile dashboard.
- `charts`: core models and chart CRUD.
- `wizard`: multi‑step flow using draft objects for persistence.
- `matrix`: 9x9 grid view/edit using **HTMX** for modals and updates.

**Tech Stack Highlights:**
- **HTMX:** Used for task detail modals and in-place updates in the matrix view.
- **Tailwind CSS:** Styling via CDN, including dark mode support.
- **Pytest:** Primary testing framework (using `pytest-django`).

### Data Model (MVP)
- `HaradaChart`:
  - `user` (FK), `title`, `target_date`, `core_goal`, `created_at`, `updated_at`
  - `is_draft` (Boolean): To track wizard progress.
  - `perspectives` (JSON) for four perspectives.
- `Pillar`:
  - `chart` (FK), `name`, `position` (1–8).
- `Task`:
  - `chart` (FK), `pillar` (FK), `title`, `description`, `frequency` (one‑time|routine), `status` (todo|in_progress|done), `position` (1–8).

### Matrix Mapping (9x9 Grid)
The chart is rendered as a 9x9 grid (81 cells) composed of nine 3x3 sub-grids:
- **Center 3x3:** Core Goal at absolute center (4,4), surrounded by the 8 Pillars.
- **Outer 8 3x3s:** Each centered on one of the 8 Pillars, surrounded by its 8 respective Tasks.
- **Logic:** Pillars are mirrored from the center 3x3 to the centers of their outer sub-grids.

### User Stories & Acceptance Criteria
1. **Registration & Login**
	- Users can register with email/username/password and log in/out.
	- Authenticated users are redirected to their dashboard.

2. **Wizard Step 1: Core Goal**
	- Users can input long‑term goal, target date, and 4 perspectives.
	- UI shows center cell updated on input.

3. **Wizard Step 2: 8 Pillars**
	- Users can input 8 pillar titles.
	- UI shows the 8 surrounding cells populated.

4. **Wizard Step 3: 64 Action Items**
	- Users input 8 tasks per pillar with a focused 3x3 view using HTMX for navigation.
	- On completion, `is_draft` is set to false and the chart is finalized.

5. **Matrix View/Edit**
	- A responsive 9x9 grid renders core goal, pillars, and tasks.
	- Clicking a task cell opens an HTMX modal to edit title/description/frequency/status.
	- Center cell shows completion % based on tasks marked done.

### TDD Implementation Plan (Todo List)
#### Environment & Setup
- [ ] Install dependencies: `django`, `django-htmx`, `pytest-django`, `pytest-factoryboy`
- [ ] Configure `pytest.ini` and `conftest.py`

#### accounts
- [ ] Write unit tests for registration, login, and logout in `Tests/unit/accounts/test_auth.py`
- [ ] Implement `accounts` app models/urls/views/templates for auth flow
- [ ] Add profile dashboard route and template

#### charts
- [ ] Write unit tests for `HaradaChart`, `Pillar`, `Task` models in `Tests/unit/charts/test_models.py`
- [ ] Write unit tests for chart creation and progress calculation in `Tests/unit/charts/test_services.py`
- [ ] Implement `HaradaChart`, `Pillar`, `Task` models and migrations
- [ ] Implement progress calculation service (Core Goal % = Tasks Done / 64)

#### wizard
- [ ] Write unit tests for draft-based state persistence in `Tests/unit/wizard/test_persistence.py`
- [ ] Implement 3-step wizard views (Core Goal -> Pillars -> Tasks)
- [ ] Use HTMX for "Zoom-in" effect during Step 3 (focused 3x3 view)

#### matrix
- [ ] Write unit tests for HTMX-based modal updates in `Tests/unit/matrix/test_views.py`
- [ ] Implement responsive 9x9 grid using CSS Grid
- [ ] Implement HTMX modals for task editing

#### integration & QA
- [ ] Add URL wiring and navigation across wizard, matrix, and dashboard
- [ ] Verify dark mode styling and responsive layout
- [ ] Manually QA MVP flows: register → wizard → matrix → edit tasks

### Definition of Done
- All unit tests passing.
- Wizard creates a chart end‑to‑end.
- Matrix view shows correct data and completion %.
- UI matches the template’s visual language and spacing.
