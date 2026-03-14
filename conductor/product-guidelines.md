# Product Guidelines - HaradaFlow

## Prose Style
- **Clarity & Brevity:** Use simple, direct language. Avoid jargon.
- **Action-Oriented:** Use active voice and imperative mood for task-related instructions.
- **Supportive Tone:** Maintain a professional and encouraging tone to help the user stay motivated.
- **Consistent Terminology:** Ensure that terms like "Matrix," "Pillar," and "Task" are used consistently throughout the application and documentation.

## User Experience (UX) Principles
- **Predictability:** Ensure that UI components (buttons, links, navigation) behave consistently.
- **Progressive Disclosure:** Present only the necessary information to the user at each stage.
- **Accessibility:** Adhere to WCAG 2.1 Level AA standards. Use high-contrast colors and descriptive labels for screen readers.
- **Immediate Feedback:** Provide visual and/or auditory feedback for every user action (e.g., toast notifications for successful task completion).
- **Mobile First:** Prioritize a high-quality experience on mobile devices.

## Performance Standards
- **Lighthouse Scores:** Maintain a minimum score of 90 in Performance, Accessibility, Best Practices, and SEO.
- **Core Web Vitals:** Ensure that Largest Contentful Paint (LCP) is under 2.5 seconds and First Contentful Paint (FCP) is under 1.8 seconds.
- **Interactivity:** Minimize Main Thread work to ensure smooth responsiveness.
- **Resource Management:** Defer non-critical third-party scripts (e.g., Clerk, HTMX) to improve initial page load times.

## Design Patterns
- **Responsive Layouts:** Use CSS Grid and Flexbox for flexible and adaptive layouts.
- **Mobile Modals:** Use bottom-sheet overlays (rounded top corners, slide-up animation) for mobile interactions to ensure thumb-reachability.
- **Safe-Area Insets:** Respect device safe areas (pb-safe, pt-safe) in all full-screen layouts to avoid content clipping.
- **Consistent Spacing:** Use a base 8px grid system for all padding and margins.
- **Color Palette:** Use a clean and professional color palette with primary, secondary, and accent colors that meet accessibility requirements.
- **Typography:** Use a legible, sans-serif font system for all text content.
