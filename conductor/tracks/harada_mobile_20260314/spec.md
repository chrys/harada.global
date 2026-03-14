# Specification - Implement mobile-responsive 64-cell Harada Matrix

## Objective
The objective of this track is to overhaul the HaradaFlow web application to ensure that the 64-cell Harada Matrix is fully functional and intuitive on mobile devices. This involves replacing the current horizontal scroll-based layout with a more focused, responsive approach (e.g., Pillar Focus with accordions or tabs).

## Functional Requirements
- **Responsive Matrix View:** 
    - On screens `< 768px`, the 9x9 grid should be replaced by a mobile-optimized view.
    - Display the Core Goal prominently at the top.
    - Use an accordion or tabbed interface to show the 8 Pillars.
    - Tapping a Pillar should expand to show its 8 associated tasks.
- **Bottom-Sheet Modals:**
    - Convert task and pillar modals into bottom-sheet overlays on mobile devices (`< 640px`).
    - Maintain standard centered dialogs for desktop views.
- **Touch Target Optimization:**
    - Ensure all interactive elements (buttons, cells, inputs) have a minimum touch target size of 44x44px.
- **Form Input Optimization:**
    - Ensure all form inputs have a minimum font size of 16px on mobile to prevent automatic zooming on iOS Safari.
- **Global Layout Improvements:**
    - Ensure consistent padding and safe-area insets on mobile devices.
    - Improve mobile navigation and drawer behavior.

## Technical Constraints
- Must be implemented using Django templates, Tailwind CSS, and HTMX.
- Should avoid introducing heavy client-side dependencies.
- Must maintain 100% feature parity with the existing desktop functionality.

## Performance & SEO Requirements
- Improve First Contentful Paint (FCP) and Largest Contentful Paint (LCP) by deferring or inlining render-blocking resources.
- Reduce unused JavaScript.
- Add meta description tags to all pages.
- Ensure zero horizontal overflow on mobile devices.
