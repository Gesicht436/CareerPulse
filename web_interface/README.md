# CareerPulse Web Interface: Modern Professional Dashboard

The **Web Interface** is the interactive gateway to the CareerPulse ecosystem. It provides a seamless, highly responsive, and visually intuitive experience for job seekers, transforming complex AI-driven data into actionable career insights.

## The Team & Development Philosophy

This module is a collaborative effort between functional architecture and aesthetic precision.

- **Primary Development**: The foundational structure, HTML architecture, API integration, and JavaScript state management are built and maintained by **Abhinav Anand (285)** and **Harsh Anand**. They handle the heavy lifting of the "how it works"—ensuring data flows correctly from the `core_engine` and that the application is robust and performant.
- **Aesthetic Refinement & Polish**: The "final polish" is handled by the **Lead Designer** Mayank, who performs the surgical fine-tuning of the User Experience. This includes:
  - **Color Palette & Typography**: Defining the emotional tone through consistent use of professional blues, deep greys, and high-readability sans-serif fonts.
  - **Component Geometry**: Precisely controlling corner rounding (border-radius), shadows, and spacing (padding/margins) to ensure a modern, floating "card-based" interface.
  - **Interactive Feedback**: Fine-tuning hover states, transition speeds, and CSS animations to make the interface feel alive and responsive.

## Technical Architecture

The interface is built as a **High-Performance Static Web Application**, utilizing modern CSS-in-JS patterns and utility-first styling to achieve a desktop-app feel within a browser.

### 1. Styling Framework: Tailwind CSS

We utilize **Tailwind CSS v4** for all styling. This allows for rapid iteration and ensures that the design refinements (the "polish") can be applied globally via utility classes.

- **`input.css`**: The source file for custom Tailwind directives and layer-specific overrides.
- **`style.css`**: The optimized, compiled output that the browser consumes.
- **Design Tokens**: We leverage a consistent set of design tokens for colors (e.g., `primary`, `secondary`, `accent`) and spacing, ensuring that a change in the "polish" phase propagates throughout every page of the application.

### 2. The Page Ecosystem (HTML Structure)

The application is partitioned into logical views, each serving a specific stage of the candidate's journey:

- **`index.html` (Landing Page)**: The first touchpoint, explaining the value proposition of CareerPulse with high-impact visuals.
- **`upload.html` (Ingestion Hub)**: A dedicated area for resume uploads, featuring drag-and-drop zones and real-time upload progress indicators.
- **`dashboard.html` (User Home)**: A centralized view showing the candidate's recent uploads, current match scores, and a high-level overview of their career progress.
- **`analyzer.html` (Deep Analysis)**: The most complex view, which visualizes the output of the `smart_match` engine—including the 4-week roadmap, skill gaps, and justification reports.
- **`search.html` (Job Discovery)**: An interface for querying the Qdrant database, allowing users to find specific roles and immediately see their match potential.
- **`login.html` & `details.html`**: Auxiliary pages for user authentication and granular job detail views.

### 3. JavaScript Orchestration (JS Layer)

The logic is written in modern **ES6+ Vanilla JavaScript**, keeping the bundle size small and the execution speed extremely fast.

- **`api.js` (The Communicator)**: Encapsulates all network logic. It uses a centralized `apiClient` to handle `fetch` requests, automatically managing headers, `FormData` for PDF uploads, and JSON parsing for responses. It also handles environment-aware base URLs (Localhost vs. Production API).
- **`upload.js`**: Manages the file picker and the multipart/form-data submission to the `core_engine/analyze` endpoint.
- **`dashboard.js` & `analyzer.js`**: Handle DOM manipulation to inject AI results into the UI. They parse the complex JSON responses from the engine and generate dynamic HTML elements like the "Matched Skills" badges and the "Career Roadmap" timeline.
- **`main.js`**: Handles global application state, navigation, and theme toggling.

## How to Run & Develop

The development environment is optimized for rapid feedback loops.

### 1. Prerequisites

- **Node.js**: Required for the Tailwind compiler and dev server.
- **NPM**: To manage dependencies.

### 2. Installation

Navigate to the `web_interface` directory and run:

```bash
npm install
```

### 3. Development Mode

To work on the interface with real-time CSS compilation and auto-reloading:

```bash
npm run dev
```

This command runs `concurrently`:

- **`watch:css`**: Listens for changes in `input.css` or any HTML/JS file and rebuilds the `style.css`.
- **`serve`**: Launches a `live-server` at `http://localhost:3000`.

### 4. The Fine-Tuning Workflow (Polish Phase)

When applying the "final polish," the designer focuses on `input.css` and the HTML class attributes. By tweaking classes like `rounded-2xl`, `shadow-soft`, or `bg-primary-600`, the designer can instantly see the aesthetic results in the browser thanks to the live-reload system.

## Design Standards

- **Corners**: Large `rounded-xl` or `rounded-2xl` for main cards, smaller `rounded-md` for buttons.
- **Depth**: Soft, multi-layered shadows (`shadow-lg`) to distinguish between the background and active content areas.
- **Typography**: Sans-serif (Inter or similar) with tight tracking and consistent line heights for maximum readability of technical job descriptions.
- **Colors**:
  - **Primary**: A deep, professional blue for action buttons and navigation.
  - **Success**: Emerald green for high match scores (>80%) and matched skills.
  - **Warning**: Amber for skill gaps or medium-level security flags.
  - **Danger**: Rose/Red for critical security flags or low match scores.

## Future Enhancements

- [ ] Dark Mode support with a switchable CSS variables layer.
- [ ] Micro-interactions using Framer Motion (if moving to React) or Web Animations API.
- [ ] PDF preview window in the analyzer view.
- [ ] PII redaction visualizer (showing what was hidden in the resume).
