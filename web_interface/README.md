# CareerPulse Web Interface: Modern Professional Dashboard & Admin Portal

The **Web Interface** is the presentation layer of the CareerPulse ecosystem. It delivers an intuitive, responsive, and aesthetically polished user experience for job seekers and system administrators, transforming complex AI-driven career telemetry into actionable insights, top 5 job recommendations, interactive job inspection modals, live announcement banners, and real-time WebRTC mentoring stages.

---

## 1. Design & UI/UX Philosophy

The interface is engineered with a focus on functional reliability, stateful API integration, and aesthetic precision:
- **Design System & Palette**: Slate backgrounds, deep violet brand accents, teal/emerald success indicators, and rose skill gap badges.
- **Typography & Geometry**: Clean Inter sans-serif typography paired with large rounded card geometry (`rounded-2xl`, `rounded-3xl`) and multi-layered elevation shadows.
- **Interactive Feedback**: Smooth CSS transitions, file drag-and-drop zones, live radial score rings, dynamic qualification filter toggling, and interactive modal dialogs.

---

## 2. Technical Stack

- **Styling Engine:** Tailwind CSS v4 (`@tailwindcss/cli`)
- **Scripting:** Vanilla JavaScript (ES6+ Modules, zero third-party client framework dependencies)
- **Real-Time Communications:** Native Browser WebSockets & `RTCPeerConnection` (WebRTC)
- **Build & Development Server:** `concurrently` listening to Tailwind CSS watcher and `live-server`

---

## 3. Page Ecosystem (HTML Structure)

| Page | File | Purpose |
| :--- | :--- | :--- |
| **Landing Page** | `public/index.html` | Hero overview, feature grid, live telemetry counters, and 1-on-1 mentorship spotlight |
| **Authentication Hub** | `public/login.html` | Interactive Sign-In and Sign-Up tab switcher with JWT session handling |
| **Admin Control Portal** | `public/admin.html` | Admin login, live hardware telemetry (CPU, RAM, Uptime), announcement publisher, feature toggles, user table, and activity audit feed |
| **Resume Upload Portal** | `public/upload.html` | Drag-and-drop PDF resume upload zone with upload progress animation |
| **Analysis Dashboard** | `public/dashboard.html` | Top 5 job match cards, radial ATS score ring, qualification filter toggle button, `#job-inspect-modal`, skill gap badges, and 4-week roadmap |
| **Direct JD Match Tool** | `public/analyzer.html` | Direct comparison tool for pasting custom job description text |
| **Semantic Job Search** | `public/search.html` | Natural language semantic job search querying the local database |
| **Job Details View** | `public/details.html` | Unabridged job description and candidate alignment profile |
| **Live WebRTC Stage** | `public/expert_call.html` | 1-on-1 video call room with real-time chat and live AI Briefing Dossier sidebar |

---

## 4. JavaScript Architecture (JS Layer)

- **`api.js`**: Centralized HTTP client managing `FormData` for PDF uploads, automatic `Authorization: Bearer <token>` header attachment, error handling, and JSON parsing.
- **`auth.js`**: Handles Sign-In / Sign-Up tab switching, form validation, `/api/v1/auth/login` and `/signup` calls, and `localStorage` session token management.
- **`admin.js`**: Powers the Admin Control Console: authentication, live telemetry polling, announcement banner publishing, maintenance/feature flag toggling, candidate account deletion, and audit log clearing.
- **`upload.js`**: Drag-and-drop file upload engine submitting resumes to `/api/v1/analyze` and redirecting to `dashboard.html`.
- **`dashboard.js` & `analyzer.js`**: Renders top 5 recommendation cards, handles interactive inspect modal opening (`openInspectModal`), educational qualification filter toggling (`handleQualificationToggle`), ATS score ring, skill badges, and timeline DOM structures.
- **`expert_call.js`**: WebRTC engine configuring `RTCPeerConnection` with STUN servers, managing media streams over WebSocket signaling (`ws://localhost:8000/api/v1/expert/ws/{room_id}`), and rendering the live AI Briefing Dossier.
- **`main.js`**: Handles responsive navigation, active route highlighting, mobile navigation menu toggle, and global top announcement banner retrieval.

---

## 5. Development & Build Instructions

```bash
cd web_interface

# Install dependencies
npm install

# Build compiled stylesheet once
npm run build:css

# Launch development environment (Tailwind watcher + Live Server)
npm run dev
```

The application runs on `http://localhost:8080` (or `http://localhost:3000`), connecting seamlessly to the backend Core Engine on `http://localhost:8000`.
