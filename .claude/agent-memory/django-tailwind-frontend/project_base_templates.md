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

`templates/partials/_messages.html` renders Django messages with conditional CSS by tag:
- `success` → `bg-emerald-50 text-emerald-700 border border-emerald-200`
- `error` → `bg-red-50 text-red-700 border border-red-200`
- `warning` → `bg-yellow-50 text-yellow-700 border border-yellow-200`
- default (info) → `bg-blue-50 text-blue-700 border border-blue-200`

`templates/partials/_sidebar.html` is included by `base_app.html`. It renders the full sidebar with logo, nav links (Dashboard, Contas, Categorias, Transações, Perfil), and logout. Active state uses `request.resolver_match.app_name`.

**Why:** `base_app.html` needs its own inner block name (`app_content`) because it overrides `content` to inject the sidebar wrapper — if children also overrode `content`, the sidebar would be lost.

**How to apply:** Public pages extend `base.html` and override `{% block content %}`. Authenticated pages extend `base_app.html` and override `{% block app_content %}`. Do not re-include `_messages.html` — they inherit it from `base.html` automatically.
