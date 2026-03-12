---
name: Sprint 8 Design System Review — Findings
description: Results and fixes applied during the Sprint 8.1 design system audit (2026-03-12)
type: project
---

Design system review (Sprint 8.1) completed on 2026-03-12.

**Three issues were found and fixed:**

1. Missing `messages.success()` calls in accounts, categories, and transactions views — all CRUD operations (create, update, delete) were silently succeeding without any user feedback flash message. Fixed by adding `messages.success()` in `form_valid()` overrides in all three view files.

2. Sidebar had no mobile responsiveness — the `w-64 shrink-0` aside occupied 256px on all screen widths including 320px mobile, leaving almost no room for content. Fixed by adding `hidden md:flex` to the aside and adding a mobile top `<header>` with icon-only nav links in `base_app.html`, visible only on `md:hidden`.

3. Categories list type display used plain styled text (`text-emerald-600 font-medium`) instead of badge pills. Fixed to use the same `inline-flex rounded-full` badge pattern used in transactions and dashboard tables.

**Why:** All three fixes are required by the design checklist: messages (8.1.4), responsiveness (8.1.2), badge consistency (8.1.1).

**How to apply:** In future QA runs, verify `messages.success()` is present in every `form_valid()` override, and check sidebar mobile classes when reviewing `base_app.html`.
