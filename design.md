# Design.md: AeroTech SEO Suite UI/UX

## 1. Design Language: Glassmorphism
The platform will utilize a **Glassmorphism** aesthetic, characterized by:
*   **Backgrounds**: Semi-transparent surfaces (blur effect) layered over a deep, dark vibrant background[cite: 1].
*   **Depth**: Subtle drop shadows and light borders to create a "floating" glass effect[cite: 1].
*   **Color Palette**: Deep midnight navy (`#0B0E14`) as the base, with neon accents (Cyan `#00F2FF` for primary actions, Magenta `#FF007A` for error/warning states).
*   **Typography**: 'Inter' or 'Geist Mono' for a clean, high-tech, readable data-heavy interface[cite: 1].

---

## 2. Global UI Elements
*   **Glass Containers**: All main content areas are `backdrop-filter: blur(12px)` cards with a 1px white-border (opacity 0.1).
*   **Buttons**: 
    *   **Primary**: Gradient fill (Cyan to Blue) with a subtle outer glow on hover.
    *   **Secondary**: Transparent glass background with a solid border that illuminates on hover.
*   **Navigation Bar**: Fixed to the left sidebar, containing icons for Dashboard, Projects, Audits, Settings, and Profile.

---

## 3. Screen Specifications

### A. Login/Authentication Screen
*   **Background**: Dynamic dark gradient with floating geometric glass shapes.
*   **Form**: Centralized glass card with inputs featuring glowing focus states.
*   **Call-to-Action**: A "Secure Login" button with a primary gradient fill.

### B. Project Overview (The Dashboard)
*   **Top Bar**: Search bar for active projects, User profile icon, and "Add New Project" button (Primary Glow).
*   **Main Body**:
    *   **Project Grid**: Glass cards for each website, displaying the current Audit Score (circular gauge), Traffic Trend (mini line chart), and "Status" (Active/Queued/Error).
*   **Interactions**: Hovering over a card reveals "View Details" and "Delete" actions.

### C. The Audit Details Page (Core View)
*   **Header**: Domain name, current date, and a "Run New Audit" button.
*   **Top Statistics (KPIs)**: Four glass tiles displaying `LCP`, `CLS`, `Total Score`, and `Pages Optimized`.
*   **Performance Chart**: A large Recharts line graph showing historical progress[cite: 1].
*   **Optimizations Panel**: A scrollable list of content blocks. Each block shows:
    *   **Left**: Original Title/Metadata.
    *   **Center**: AI-Optimized result.
    *   **Right**: "Apply" button (Cyan) vs. "Ignore" button (Ghost).
*   **Task Status Bar**: A slim glass strip at the bottom showing the `audit_tasks` progress percentage[cite: 1].

### D. Settings & Configuration
*   **Layout**: Tabbed navigation (General, API Keys, Subscription, Usage Logs).
*   **Content**: Inputs for Google Search Console/Analytics tokens; usage meter progress bars (`UsageTracker` data) displaying limits[cite: 1].

---

## 4. UI/UX Interaction Rules
*   **Transitions**: All UI changes (tab switches, opening modals) use smooth `fade-in` and `slide-up` animations.
*   **Feedback Loops**:
    *   **Loading**: Skeleton loaders (shimmer effect) inside glass cards while data fetches.
    *   **Success**: Subtle notification toast (glass style) appearing in the top-right.
    *   **Errors**: Error messages appear as a pulse-red border around the relevant glass component[cite: 1].

---

## 5. Accessibility & Responsiveness
*   **Responsive Breakpoints**: The glass panels stack vertically on mobile (narrow) devices.
*   **Contrast**: High-contrast text (white/light grey) against the deep glass background to ensure readability in all lighting conditions[cite: 1].