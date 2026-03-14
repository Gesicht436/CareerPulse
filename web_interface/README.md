# Web Interface (`web_interface/`)

The **CareerPulse Web Interface** is a modern, high-performance frontend built with Next.js 15+ and Tailwind CSS v4. It focuses on a "Security-First" UI/UX for secure resume analysis.

---

## 1. Technical Stack

- **Framework:** Next.js 15+ (App Router)
- **Styling:** Tailwind CSS v4 + shadcn/ui
- **State Management:** Zustand
- **Icons:** Lucide-React
- **Notifications:** Sonner

---

## 2. Architecture: Atomic Design

We follow an **Atomic Design** structure to ensure scalability and reusability:

- **Atoms:** Basic UI components from shadcn (Button, Input, Card).
- **Molecules:** Composite components (e.g., `FileUploadZone`).
- **Organisms:** Complex UI blocks (e.g., `Navbar`).
- **Templates:** Layout structures for different page types.
- **Pages:** The actual Next.js routes (`/`, `/upload`, `/dashboard`).

---

## 3. Key Progress

- [x] **Project Scaffolding:** Initialized with Next.js, TS, and Tailwind v4.
- [x] **Atomic Structure:** Created directories for molecules, organisms, hooks, and stores.
- [x] **Global State:** Implemented `useResumeStore` and `useUIStore` with Zustand.
- [x] **Secure Upload:** Built the `FileUploadZone` molecule with real-time feedback.
- [x] **Responsive Design:** Centered and balanced layout for home, upload, and dashboard pages.

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

The frontend will be available at `http://localhost:3000`.

---

## 5. Roadmap

1. **Client-Side Redaction:** Implement regex-based PII redaction before file upload.
2. **Analysis Dashboard:** Integrate interactive charts (Recharts) for match results.
3. **Real-time Feedback:** Show progressive analysis steps from the backend.
