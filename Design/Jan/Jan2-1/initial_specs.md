# Product Requirement Document (PRD): Harada Method Builder

## 1. Executive Summary

**Project Name:** HaradaFlow

**Objective:**
A Django-based web application designed to help individuals achieve self-reliance by digitizing the Harada Method 64-cell matrix and long-term goal-setting process.

## 2. User Personas

- **The Striver:** Someone with a massive goal (like launching a website) who feels overwhelmed by the scale of the task.
- **The Coach:** Someone using the framework to guide a team or mentee.

## 3. Functional Requirements
### 3.1 Authentication & Profile

- **FR1:** User Registration (Email, Username, Password)
- **FR2:** User Login/Logout
- **FR3:** Profile Dashboard: View all active and archived Harada Charts

### 3.2 The Harada Wizard (Core Feature) 🪄

To make the 64-cell task less daunting, the wizard must be incremental.

**Step 1: The Core Goal (The "Why")**

- **Left Panel:** Asks for the Long-Term Goal, Target Date, and the "Four Perspectives" (Self-Tangible, Self-Intangible, etc.)
- **Right Panel:** Visualizes the center square of the 9x9 grid

**Step 2: The 8 Pillars**

- **Left Panel:** Prompts for 8 high-level themes (Technical, Mental, etc.)
- **Right Panel:** Populate the 8 squares immediately surrounding the center

**Step 3: The 64 Action Items**

- **Left Panel:** Focuses on one pillar at a time. "Let's brainstorm 8 tasks for [Pillar Name]."

**Right Panel:** Zooms into that specific 3x3 sub-grid to reduce visual noise.

3.2 The Harada Wizard (Core Feature) 🪄
To make the 64-cell task less daunting, the wizard must be incremental.

Step 1: The Core Goal (The "Why"):

Left Panel: Asks for the Long-Term Goal, Target Date, and the "Four Perspectives" (Self-Tangible, Self-Intangible, etc.).

Right Panel: Visualizes the center square of the 9x9 grid.

Step 2: The 8 Pillars:

Left Panel: Prompts for 8 high-level themes (Technical, Mental, etc.).

Right Panel: Populate the 8 squares immediately surrounding the center.

Step 3: The 64 Action Items:

Left Panel: Focuses on one pillar at a time. "Let's brainstorm 8 tasks for [Pillar Name]."

Right Panel: Zooms into that specific 3x3 sub-grid to reduce visual noise.


### 3.3 The Interactive Matrix (The View/Edit Mode)

- **FR4:** Responsive Grid: A 9x9 interactive grid
- **FR5:** Cell Interactivity: Clicking any of the 64 action cells opens a "Detail Modal"
	- **Fields:** Task Title, Description, Frequency (One-time vs. Daily Routine), and Status (Todo/In Progress/Done)


- **FR6:** Progress Visualization: The center goal square should show a percentage (%) completion based on the 64 sub-tasks

### 3.4 Data Management

- **FR7:** Edit/Update: Users can modify titles or descriptions at any time
- **FR8:** Delete: Full deletion of a chart with a "Confirmation" safety step
- **FR9:** Export (v1.1): Option to export the 64-cell chart as a PDF or CSV


## 5. BA Suggestions for "Value Add" 📈

As a Senior BA, you might consider these "Phase 2" requirements to make the site more "Harada-compliant":

- **The Daily Checksheet:** Since Pillar 3 is "Routine," the app should generate a "Daily To-Do" list based on the tasks marked as "Routine" in the 64-cell chart
- **Soji Reminder:** A simple notification or checkbox for "Mental/Physical Cleaning" to keep the user aligned with the 5th pillar
- **Color Coding:** Allow users to color-code pillars (e.g., Technical = Blue, Health = Green) for better visual scanning

