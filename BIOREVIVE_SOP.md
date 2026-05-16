# BioRevive Lab - Standard Operating Procedures (SOP)

## 1. CEO Vision & Brand Identity
*   **Brand Positioning:** Premium, trustworthy, and scientific. We provide luxury, professional-grade microbial solutions for sustainable wastewater treatment (BCG Model).
*   **Target Audience:** Luxury hotels, high-end restaurants, and environmentally conscious B2B enterprises.

## 2. Design Guidelines (UI/UX)
*   **Color Palette:**
    *   Primary: Deep Navy (`#0F0F1A`, `#1a1a2e`)
    *   Accent: Premium Gold (`#D4AF37`, `#06C755` for success/action)
    *   Text: White and Light Gray for readability on dark backgrounds.
*   **Typography:**
    *   English: `Outfit`, `Inter`
    *   Thai: `Noto Sans Thai`
*   **Aesthetics:** Dark mode, glassmorphism UI, clean and minimalist layouts. Avoid generic colors.

## 3. Technical Architecture (3-Layer System)
*   **Directive Layer:** This SOP file governs all agentic actions and coding standards.
*   **Orchestration Layer:** AI task management utilizing a 3-Lane structure.
*   **Execution Layer:** Code implementation adhering to the following rules:
    *   **Frontend (Lane 1):** HTML/JS with Vanilla CSS. Mobile-responsive, dynamic interfaces.
    *   **Backend (Lane 2):** SQLite (`app.sqlite`) via local Open Design Daemon. No third-party backend unless explicitly requested.
    *   **Marketing (Lane 3):** Automated image composition and Facebook automation using Composio/Python scripts.

## 4. Work Lanes (Task Clustering)
1.  **Lane 1: Frontend (Web UI & Dashboard)**
    *   Landing Page, Dashboard, Usage Guide (Dosage Calculator), Pitch Decks.
2.  **Lane 2: Backend (Database & APIs)**
    *   Product catalog, dosage formulas, calculation history.
3.  **Lane 3: Marketing (Ads & Social Media)**
    *   Product posters, Facebook captions, promotional sets.

## 5. Development Rules
*   Never overwrite the Open Design Daemon source code without explicit permission.
*   Ensure all new frontend pages link back to `dashboard.html`.
*   Prioritize self-correction: If a script fails, read the logs and fix it before reporting to the CEO.
