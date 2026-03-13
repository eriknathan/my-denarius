---
name: Base templates created
description: Records which root templates exist, their block names, messages partial placement, and inheritance rules
type: project
---

`templates/base.html` is the root HTML5 layout. It defines three blocks:
- `{% block title %}` — page title (defaults to "my-denarius")
- `{% block content %}` — main page body
- `{% block extra_js %}` — scripts at the bottom of <body>

It includes TailwindCSS via CDN (`https://cdn.tailwindcss.com`), Inter via Google Fonts (weights 300–700), and applies `font-family: 'Inter', sans-serif` via a `<style>` tag. Body has `bg-gray-50 text-gray-800 antialiased`.

`{% include 'partials/_messages.html' %}` is placed inside a `<div class="max-w-7xl mx-auto px-4 pt-4">` wrapper directly in `<body>` before `{% block content %}`, so every page inheriting `base.html` automatically shows Django messages with consistent horizontal padding.

`templates/base_app.html` extends `base.html` and overrides `{% block content %}` to create the sidebar layout (`flex min-h-screen`). It includes `partials/_sidebar.html` and defines `{% block app_content %}` for child templates to fill. **Child templates that extend `base_app.html` must override `{% block app_content %}`, not `{% block content %}`.**

`templates/partials/_messages.html` renders Django messages with:
- `data-message` attribute on each message div (used by auto-dismiss JS)
- `flex items-start gap-3` layout with a close button (×) on the right
- Auto-dismiss after 4 seconds via `dismissMessage()` JS function inside the partial
- Dark mode variants on all colors: e.g. `dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800`
- Tags: success/error/warning/default(info)

`templates/partials/_sidebar.html` is included by `base_app.html`. It renders the full sidebar with logo, nav links (Dashboard, Contas, Categorias, Transações, Perfil), and logout. Active state uses `request.resolver_match.app_name`.

## Delete confirmation modal (base_app.html)
- Modal `id="delete-modal"` lives inside `{% block content %}` in `base_app.html`, placed after the main layout div but before `{% endblock %}`
- JS functions `openDeleteModal(url, title, body)` and `closeDeleteModal()` are in `{% block extra_js %}`
- Escape key handler is consolidated — closes both modal and sidebar
- List pages call `openDeleteModal()` from `<button type="button" onclick="...">` instead of linking to the confirm_delete URL

## Dark mode toggle (public pages)
Pages extending `base.html` that need a theme toggle:
- Add `relative` to the outermost container div
- Place `<div class="absolute top-4 right-4">` with sun/moon button
- Sun SVG: `id="theme-icon-light"` (starts `hidden`); Moon SVG: `id="theme-icon-dark"` (visible)
- Add `{% block extra_js %}` with DOMContentLoaded listener to sync icons, and a wrapper around `window.toggleTheme` to toggle icons on click
- `home.html`: toggle button is in the navbar flex row instead (not absolute positioned)

**Why:** `base_app.html` needs its own inner block name (`app_content`) because it overrides `content` to inject the sidebar wrapper — if children also overrode `content`, the sidebar would be lost.

**How to apply:** Public pages extend `base.html` and override `{% block content %}`. Authenticated pages extend `base_app.html` and override `{% block app_content %}`. Do not re-include `_messages.html` on list/form pages that already inherit from base — it's injected by `base.html` at the top of every page. Individual templates that include `_messages.html` explicitly (like login, accounts/list) are intentional for positioning it close to the form/action area.
