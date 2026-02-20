# Web Interface (`web_interface/`)

The **CareerPulse Web Interface** is a modern, high-performance frontend designed to provide job seekers with an intuitive and secure environment to analyze their resumes against market standards.

---

## 1. Technical Stack

- **Framework:** Next.js (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS + shadcn/ui
- **State Management:** Zustand
- **Form Handling:** React Hook Form + Zod (Validation)
- **Data Visualization:** Recharts / ECharts
- **HTTP Client:** Axios / TanStack Query (React Query)

---

## 2. Work Distribution

### **Abhinav 285 (Lead Developer)**

- **Component Architecture:** Setting up the atomic design structure, layout, and reusable UI components.
- **State Management:** Implementing global state using Zustand for user sessions and application-wide settings.
- **Secure File Upload:** Implementation of the drag-and-drop resume upload system.
- **Client-Side Privacy:** Integrating logic for PII (Personally Identifiable Information) redaction *before* the file is transmitted to the server.
- **API Integration:** Establishing robust hooks to communicate with the `core_engine` REST endpoints.

### **Harsh (Data Visualization Specialist)**

- **Career Readiness Dashboard:** Building interactive charts to display match percentages and skill rankings.
- **Skill-Gap Heatmaps:** Developing visual representations of missing competencies and industry demand.
- **User Experience (UX):** Ensuring the interface is responsive, accessible, and follows a "Security-First" aesthetic.
- **Reporting Interface:** Designing the UI for "Explainable AI" feedback, providing users with actionable learning paths.

---

## 3. Key Feature Requirements

1. **Zero-Trust Uploads:** Visual indicators confirming that PII has been redacted locally before upload.
2. **Adversarial Feedback:** UI notifications that inform the user if "Resume Smuggling" or prompt injection attempts were detected during processing.
3. **Real-time Analysis:** Progressive loading states while the RAG engine processes the resume against Job Descriptions.
4. **Interactive Career Pathing:** A roadmap visualization based on the skill-gap analysis.

---

## 4. Development Setup

```bash
# Navigate to the directory
cd web_interface

# Install dependencies
npm install

# Start development server
npm run dev
```

*Refer to the root [ARCHITECTURE.md](../ARCHITECTURE.md) for global project standards and Git workflows.*
