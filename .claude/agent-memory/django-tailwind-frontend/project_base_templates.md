---
name: Base templates created
description: Records which root templates exist, their block names, and the partials they depend on
type: project
---

`templates/base.html` is the root HTML5 layout. It defines three blocks:
- `{% block title %}` — page title (defaults to "my-denarius")
- `{% block content %}` — main page body
- `{% block extra_js %}` — scripts at the bottom of <body>

It includes TailwindCSS via CDN (`https://cdn.tailwindcss.com`), Inter via Google Fonts, and applies `font-family: 'Inter', sans-serif` with a `<style>` tag. Body has `bg-gray-50 text-gray-800 antialiased`.

`{% include 'partials/_messages.html' %}` is placed directly inside `<body>` before `{% block content %}`, so every page inheriting `base.html` (including `base_app.html`) automatically shows Django messages.

`templates/partials/_messages.html` renders the Django messages framework output with emerald/red/blue styling per tag (success / error / default).

**Why:** `base_app.html` (sidebar layout) will extend `base.html`, so messages must live at the root level to avoid re-including the partial in every child template.

**How to apply:** When building authenticated-area templates, extend `base_app.html`, not `base.html` directly. Never re-include `_messages.html` in templates that already inherit from `base.html`.
