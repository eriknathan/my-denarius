---
name: Responsive design patterns
description: Mobile-first responsive conventions applied across all my-denarius templates, including sidebar drawer, card-vs-table patterns, and button stacking rules
type: project
---

The project was made fully responsive (mobile, tablet, desktop) in March 2026. Key decisions:

## Sidebar / navigation

- Desktop sidebar: `hidden md:flex w-64` fixed left column in `_sidebar.html`
- Mobile sidebar: `fixed` drawer `#mobile-sidebar` with `transform -translate-x-full transition-transform duration-300` toggled by `openSidebar()` / `closeSidebar()` vanilla JS in `base_app.html`'s `{% block extra_js %}`
- Shared nav markup lives in `templates/partials/_sidebar_nav.html` (new partial), included by both `_sidebar.html` instances
- Mobile topbar: hamburger on the left, logo centered, "+ transaction" quick-action on the right; `sticky top-0 z-10`
- Overlay: `#sidebar-overlay` closes drawer on backdrop click; Escape key also closes

**Why:** The old mobile nav was icon-only tab bar with no labels — unusable for new users.

## Tables vs cards pattern

- `< sm` (< 640 px): card layout (`sm:hidden`)
- `>= sm` (tablets): table layout (`hidden sm:block`) for accounts/categories
- `< md` (< 768 px): card layout (`md:hidden`) for transactions list (7-column table is too wide)
- `>= md`: table for transactions (`hidden md:block`)

Each table also has `overflow-x-auto` as a safety net.

## Buttons and forms

- Form action buttons: `flex-col sm:flex-row gap-3` so they stack full-width on mobile, side-by-side on sm+
- Button touch target: `py-2.5` on mobile reduced to `py-2` on `sm:`
- CTA buttons in list page headers: icon-only on mobile (`hidden sm:inline` for label text) via `<span class="hidden sm:inline">`
- Forms: `max-w-lg` constrains width on desktop; on mobile they naturally span full width

## Dashboard metric cards

- Grid: `grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6` (2 columns on mobile, 4 on desktop)
- Card content: smaller text/icons on mobile (`text-lg sm:text-2xl`, `w-4 h-4 sm:w-6 sm:h-6`)
- Subtitle text hidden on mobile: `hidden sm:block`

## Profiles detail

- Changed from `flex items-center justify-between` per-row to stacked label-above-value layout (`<p class="text-xs ...">label</p><p>value</p>`) — the old layout broke at narrow widths
- Email uses `break-all` to prevent overflow

## Public home

- Nav: `gap-2 sm:gap-3`, `px-3 sm:px-4` — prevents buttons wrapping on tiny screens
- Hero text: `text-3xl sm:text-5xl`
- Feature cards: `grid-cols-1 sm:grid-cols-3`

## Register form

- Name/surname grid: `grid-cols-1 sm:grid-cols-2` (was `grid-cols-2` which was too cramped on mobile)

**How to apply:** Any new list template with >= 4 columns should use table on md+ and card layout on smaller screens. Any delete/form page buttons should use `flex-col sm:flex-row`.
