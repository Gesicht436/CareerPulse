# CareerPulse Web Interface: Modern Professional Dashboard & Admin Portal

The **Web Interface** is the interactive gateway to the CareerPulse ecosystem. It provides a seamless, highly responsive, and visually intuitive experience for job seekers and system administrators, transforming complex AI-driven data into actionable career insights, user authentication, top 5 job recommendations, full job description inspection modals, live announcement banners, and real-time WebRTC mentoring stages.

---

## Development & UI/UX Philosophy

The web interface is engineered by **Mayank Anand** with a focus on functional reliability, stateful API integration, and aesthetic precision:

- **Color Palette & Typography**: Professional violet, slate, and teal tones paired with high-readability Inter sans-serif fonts.
- **Component Geometry**: Precise control over corner rounding (`border-radius`), glassmorphic panels, and elevated card shadows.
- **Interactive Feedback**: Smooth hover transitions, live progress bars, tab switchers, inspection modals, qualification filter toggles, and responsive stage layouts.

---

## Technical Architecture

Built as a **High-Performance Web Application** utilizing utility-first styling with Tailwind CSS v4 and modern ES6+ Vanilla JavaScript.

### 1. Styling Framework: Tailwind CSS v4

- **`input.css`**: Source file for custom Tailwind directives, glassmorphism utilities (`glass-panel`), and custom scrollbars.
- **`style.css`**: Compiled output consumed by the browser.
- **Design Tokens**: Standardized design tokens across colors, border radii, and elevated card shadows.

### 2. Page Ecosystem (HTML Structure)

- **`index.html` (Landing Page)**: Introduces CareerPulse capabilities with interactive tool cards, telemetry counters, and 1-on-1 mentorship spotlight.
- **`login.html` (Authentication Hub)**: Interactive Sign-In and Sign-Up tab switcher interface with real-time alert banners.
- **`admin.html` (Admin Control Hub)**: Admin login modal (`admin@careerpulse.ai`), telemetry metrics dashboard, live announcement banner publisher, feature flags toggling, candidate user table, and activity audit feed.
- **`upload.html` (Ingestion Hub)**: Drag-and-drop resume upload zone with live upload progress feedback.
- **`dashboard.html` (Career Dashboard)**: Top 5 recommendation cards, educational qualification filter control bar with toggle button, `#job-inspect-modal` full job description modal, radial ATS score ring, strategic justifications, skill gap badges, and 4-week roadmap timeline.
- **`analyzer.html` (Direct Job Match)**: Tool for pasting custom job description text and evaluating match scores on demand.
- **`search.html` (Job Discovery)**: Natural language semantic search view querying the local Qdrant database.
- **`details.html`**: Unabridged job details and candidate profile setup view.
- **`expert_call.html` (Live WebRTC Stage)**: Real-time 1-on-1 peer-to-peer video/audio call stage with in-call chat and live AI Expert Briefing Dossier sidebar.

### 3. JavaScript Orchestration (JS Layer)

- **`api.js` (Centralized Client)**: Manages network requests via `apiClient`, managing `FormData` for PDF uploads, attaching `Authorization: Bearer <token>` headers, and parsing JSON responses.
- **`auth.js` (Auth Engine)**: Manages Sign-In / Sign-Up tab navigation, form validations, API calls (`/api/v1/auth/login` & `/signup`), and `localStorage` session token storage.
- **`admin.js` (Admin Engine)**: Powers admin authentication, live telemetry fetching, announcement banner publishing, feature toggling, user deletion, and audit log clearing.
- **`upload.js`**: File picker, drag-and-drop handlers, and `/api/v1/analyze` execution.
- **`dashboard.js` & `analyzer.js`**: Renders top 5 recommendation cards, handles interactive inspect modal opening (`openInspectModal`), educational qualification filter toggling (`handleQualificationToggle`), ATS score ring, skill badges, and timeline DOM structures.
- **`expert_call.js` (WebRTC Engine)**: Configures `RTCPeerConnection` with STUN servers, manages audio/video track negotiation over WebSocket signaling (`ws://localhost:8000/api/v1/expert/ws/{room_id}`), and renders the AI Briefing Dossier.
- **`main.js`**: Unified navigation bar handling, active link state highlighting, mobile menu toggle, and global top announcement banner fetch & render.

---

## How to Run & Develop

```bash
cd web_interface
npm install
npm run build:css
npm run dev
```

Runs `concurrently` listening for Tailwind changes (`watch:css`) and launching a `live-server` on `http://localhost:3000`.

---

## Design Standards

- **Corners**: Large `rounded-xl` / `rounded-2xl` / `rounded-3xl` for floating cards.
- **Depth**: Soft, multi-layered elevation shadows (`shadow-lg`, `shadow-2xl`).
- **Typography**: Clean sans-serif typography (Inter) for high readability.
- **Colors**:
  - **Primary**: Deep violet for primary actions, auth tabs, and stage highlights.
  - **Success**: Teal/Emerald for verified matched skills, high scores, and live 1-on-1 mentorship callouts.
  - **Warning / Missing**: Rose/Red for missing skill gaps.
