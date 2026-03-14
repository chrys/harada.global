# Implementation Plan - Implement mobile-responsive 64-cell Harada Matrix

## Phase 1: Foundation & SEO (Global Improvements) [checkpoint: 434f523]
- [x] Task: Add Meta Description tags to `templates/base.html` and other key pages. (57fb72d)
- [x] Task: Implement global mobile padding and safe-area insets in `templates/base.html`. (6a5bd43)
- [x] Task: Ensure all interactive elements meet the 44x44px touch target requirement. (b887437)
- [x] Task: Update all form inputs to `text-[16px]` for mobile responsiveness. (3a081e1)
- [x] Task: Conductor - User Manual Verification 'Phase 1: Foundation & SEO' (434f523)

## Phase 2: Responsive Matrix View Overhaul
- [x] Task: Research and implement a mobile-optimized view for the 9x9 grid in `templates/matrix/view.html` (e.g., Pillar Accordion). (267bfc5)
- [x] Task: Remove horizontal scroll dependency for the matrix on screens `< 768px`. (267bfc5)
- [x] Task: Ensure HTMX interactions (adding/editing tasks) work seamlessly in the new mobile view. (267bfc5)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Responsive Matrix View Overhaul'

## Phase 3: Mobile Modals (Bottom Sheets)
- [ ] Task: Refactor `templates/matrix/*_modal.html` to implement bottom-sheet behavior on mobile (`< 640px`).
- [ ] Task: Ensure transition animations are smooth and consistent across mobile and desktop.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Mobile Modals'

## Phase 4: Performance Optimization
- [ ] Task: Identify and defer/inline render-blocking CSS and JS in `templates/base.html`.
- [ ] Task: Audit and reduce unused JavaScript.
- [ ] Task: Verify LCP and FCP improvements using Lighthouse.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Performance Optimization'
