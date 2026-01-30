## MVP (Completed)

- [x] **User Management (Clerk Integration)**
    - Seamless authentication with Clerk (Login, Register, Logout).
    - Custom `ClerkMiddleware` for JWT verification and Django user synchronization.
    - Context processors for consistent frontend user state.
- [x] **Core Data Model**
    - `HaradaChart`: Handles core goals, target dates, and 64-cell completion logic.
    - `Pillar`: 8 high-level themes per chart with customizable colors.
    - `Task`: 64 action items (8 per pillar) with status and frequency tracking.
- [x] **3-Step Guided Wizard**
    - **Step 1: Core Goal:** Define title, goal, date, and 4 perspectives (Self/Others x Tangible/Intangible).
    - **Step 2: 8 Pillars:** Break down the core goal into 8 foundational pillars.
    - **Step 3: 64 Tasks:** Populate each pillar with 8 specific action items using a focused UI.
    - **Session Persistence:** Unauthenticated users can start a chart; progress is saved in sessions and migrated to the database upon sign-up.
- [x] **Interactive 9x9 Matrix**
    - Responsive 9x9 grid visualization using deterministic mapping logic.
    - **Pillar Mirroring:** Central pillars are automatically mirrored to the centers of outer 3x3 grids.
    - **Real-time Updates:** HTMX-powered modals for editing tasks and pillars without page reloads.
    - **Progress Tracking:** Automatic completion percentage calculation displayed at the core.
- [x] **Tech Stack & UI/UX**
    - **Django 6.0 & Python 3.12:** Robust backend foundation.
    - **HTMX:** For smooth, reactive UI interactions.
    - **Tailwind CSS:** Modern, responsive design with full Dark Mode support.
    - **TDD:** Comprehensive test suite using Pytest and FactoryBoy.
- [x] **Educational Content**
    - Dedicated pages explaining the Harada Method (Long Term Goal, Five Pillars, 64 Tasks).

## Phase 2 (In Progress)

### 1. Updated Main Menu
- 1.1 Features
- 1.2 Use Cases
- 1.3 Method
- 1.4 Examples
