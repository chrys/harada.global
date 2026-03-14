# PRD: HaradaFlow Mobile Responsive Overhaul

## 1. Executive Summary & Objective
The goal of this initiative is to make the HaradaFlow web application fully mobile-friendly. While the app currently utilizes Tailwind CSS for some basic responsiveness (e.g., stacked columns on the homepage and a hamburger menu), the core feature—the 64-cell Harada Matrix—is not optimized for mobile devices. It relies on a horizontally scrollable overflowing container, which degrades the user experience. We need to create a seamless, intuitive, and highly responsive mobile experience across all views.

## 2. Current State & Pain Points
* **The Matrix View**: The 9x9 grid in `matrix/view.html` forces a `min-width: 720px` to maintain the 64-task layout. On mobile, users see a "← Scroll to see full matrix →" helper text and must pan horizontally to view and interact with the grid.
* **Modals**: The various task and pillar modals (`task_create_modal.html`, `task_modal.html`, `pillar_modal.html`) might not be optimized as full-screen or bottom-sheet overlays on mobile, leading to cut-off content or awkward scrolling.
* **Navigation & Padding**: While a mobile nav exists, touch targets and padding on inner pages might be too small or restrictive on smaller screens.
* **Wizard Flow**: The wizard (`/wizard/*`) needs to be verified for proper padding, input text sizes (to prevent iOS auto-zoom), and button placements.
* **Performance & SEO**: Lighthouse reports highlight slow First Contentful Paint (2.5s) and Largest Contentful Paint (3.9s) due to render-blocking requests and unused JavaScript. Additionally, the site currently lacks meta descriptions for content best practices.

## 3. High-Level Requirements

### 3.1. The 64-Cell Matrix Mobile Experience
Instead of forcing a cramped 9x9 view, the mobile Matrix view should adopt a more focused layout.
* **Proposed Approach A (Pillar Focus)**: On mobile (`< 768px`), display the Core Goal prominently at the top, followed by an accordion or tabbed list of the 8 Pillars. Tapping a Pillar expands to show its specific 8 tasks in a vertical or 2x4 grid.
* **Proposed Approach B (Mini-Map / Kanban)**: Treat the matrix like a canvas where the user can pinch-to-zoom, or provide a list-view toggle specifically for mobile devices.
* *Requirement*: Remove horizontal scrolling dependence for interacting with tasks on mobile.

### 3.2. Responsive Modals (Bottom Sheets)
* **Mobile Modals**: Convert standard centered modals into "Bottom Sheets" on mobile devices (screens `< 640px`). They should slide up from the bottom, take up 100% of the screen width, and have a swipe-down or clear "X" close affordance.
* **Desktop Modals**: Remain as centered dialogs.

### 3.3. Touch Targets & Form Inputs
* **Actionable Items**: Ensure all buttons, links, matrix cells, and form inputs meet the minimum 44x44px touch target recommendation.
* **Form Inputs**: Ensure text `<input>` and `<textarea>` elements have at least `text-[16px]` on mobile to prevent iOS Safari from automatically zooming in when focused.

### 3.4. Navigation & Layout
* **Global Padding**: Use safe-area insets and consistent mobile padding (`px-4` vs desktop `px-8`).
* **Header/Footer**: Ensure the hamburger menu functions smoothly and the Clerk authentication buttons (`user-button-mobile`) fit properly inside the mobile drawer.

### 3.5. Performance & SEO
* **Render-Blocking Requests**: Defer or inline CSS/JS files that block initial rendering to improve First Contentful Paint (FCP) from its current 2.5s.
* **Largest Contentful Paint (LCP)**: Optimize initial loading to bring LCP down from its current 3.9s.
* **JavaScript Optimization**: Reduce unused JavaScript to free up the main thread and improve load times.
* **Meta Attributes**: Add `<meta name="description" content="...">` to all pages meeting SEO best practices.

## 4. Scope of Work (Affected Files)
1. `templates/matrix/view.html`: Overhaul matrix grid CSS/layout specifically for the `< md` breakpoint. Implement a list/accordion mobile view override.
2. `templates/matrix/*_modal.html`: Refactor modal container classes to implement bottom-sheet behavior on mobile.
3. `templates/wizard/*.html`: Review inputs and buttons for mobile sizes.
4. `templates/base.html`: Polish mobile navigation and ensure no horizontal overflow occurs globally.

## 5. Definition of Done
* The 64-cell matrix can be fully managed (tasks added, edited) on a standard mobile screen (e.g., 375px width) without horizontal scrolling.
* Modals open cleanly as bottom sheets or full-screen overlays on mobile.
* Google Chrome Lighthouse "Mobile Friendly" score passes with no text-size or touch-target errors.
* Lighthouse Performance issues are addressed: FCP/LCP metrics improved, render-blocking eliminated/deferred, unused JS reduced.
* Each page includes a valid Meta Description tag for SEO.
* No horizontal layout shifting or unintended side-scrolling across the entire application.
