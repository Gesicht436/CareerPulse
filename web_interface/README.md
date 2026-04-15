# CareerPulse Web Interface (Vanilla HTML/JS)

This is the privacy-first, simplified frontend for **CareerPulse**, built with pure HTML5, JavaScript (ES Modules), and Tailwind CSS v4.

---

## Standard Operating Procedure (SOP) for Teammates

Welcome to the CareerPulse UI team! Follow these steps to set up your local development environment and start contributing.

### 1. Prerequisites

Ensure you have the following installed on your machine:

- **Node.js** (v18.0.0 or higher)
- **npm** (comes with Node.js)
- **Git**

### 2. Initial Setup

Open your terminal and run the following commands:

```bash
# Navigate to the web interface directory
cd web_interface

# Install all development dependencies
npm install
```

### 3. Running the Development Environment

To start working, run the development script. This will launch a hot-reloading server and start the Tailwind CSS compiler in watch mode.

```bash
npm run dev
```

- **Local Website:** [http://127.0.0.1:3000](http://127.0.0.1:3000)
- **Hot Reloading:** The page will automatically refresh when you save changes to any HTML or JS file.
- **Auto-CSS:** Tailwind will detect new classes in your HTML and rebuild the CSS automatically.

---

## Tech Stack & Tools

- **HTML5:** Semantic markup for all pages.
- **JavaScript (ES Modules):** Modular Vanilla JS (no heavy frameworks).
- **Tailwind CSS v4:** Modern styling via CLI compiler.
- **Concurrently:** Runs the server and CSS watcher in one terminal window.
- **Live-Server:** Lightweight development server.

---

## Project Structure Guide

All development happens inside the `src/` directory.

### HTML Pages (`src/`)

- `index.html`: The Landing Page (entry point).
- `login.html`: User authentication page.
- `details.html`: Personal profiling and career goals form.
- `upload.html`: Resume upload and analysis trigger.
- `dashboard.html`: The main analysis results overview.
- `search.html`: Job and company search interface.
- `analyzer.html`: Individual Job Description (JD) analyzer.

### Assets & Logic

- `src/css/input.css`: The source CSS file (where `@import "tailwindcss";` lives).
- `src/css/output.css`: **[DO NOT EDIT]** Auto-generated CSS file linked in HTML.
- `src/js/`:
  - `api.js`: Centralized API client for backend communication.
  - `main.js`: Logic for the landing page.
  - `upload.js`: Logic for file selection, drag-and-drop, and upload.
  - `dashboard.js`: Logic for rendering analysis results.

---

## Development Workflow

1. **Edit HTML:** Add your markup to any file in `src/`. Use Tailwind utility classes directly in the `class` attribute.
2. **Add Logic:** Create or edit scripts in `src/js/`. Always use `type="module"` when linking scripts in HTML.
3. **Check Styling:** If you add a new Tailwind class, the watcher started by `npm run dev` will automatically include it in `src/css/output.css`.
4. **Backend Integration:** Use the `apiClient` in `src/js/api.js` to fetch data from the FastAPI backend.

---

## Building for Production

To generate a minified, optimized CSS file for deployment:

```bash
npm run build
```

---

## API Integration

The `src/js/api.js` file is configured to switch between local and production API endpoints automatically.

```javascript
import { apiClient } from './api.js';

// Example: Fetching search results
const results = await apiClient.get('/smart_match/search?query=developer');
```
