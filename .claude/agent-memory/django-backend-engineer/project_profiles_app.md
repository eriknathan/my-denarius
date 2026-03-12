---
name: profiles app architecture
description: Profile model, post_save signal, admin, and AppConfig.ready() wiring for the profiles app
type: project
---

The `profiles` app owns a single `Profile` model with a OneToOne relation to `AUTH_USER_MODEL`.

**Why:** Every user gets a profile automatically so extra user data (phone, future fields) lives separately from the auth model.

**How to apply:** When adding new per-user data fields, extend `Profile` here rather than touching the `users.User` model.

## Key decisions

- `Profile.user` is a `OneToOneField` with `related_name='profile'` — access via `request.user.profile`
- Signal `create_user_profile` lives in `profiles/signals.py`, connected via `ProfilesConfig.ready()` in `profiles/apps.py`
- Signal sender is `settings.AUTH_USER_MODEL` (string), not `get_user_model()`, so it fires correctly at startup
- `class Meta: ordering = ['user__email']`
- `__str__` returns `'Perfil de {user.email}'` (Portuguese UI string)
- Migration: `profiles/migrations/0001_initial.py`
- Admin: `ProfileAdmin` with `list_display`, `list_filter`, `search_fields`, `raw_id_fields`

## Views and URLs (Sprint 7)

- `ProfileDetailView`: `LoginRequiredMixin + DetailView`, overrides `get_object()` to return `request.user.profile`. Template: `profiles/detail.html`.
- `ProfileUpdateView`: `LoginRequiredMixin + View` (plain `View`, not `UpdateView`) — handles two forms simultaneously. Overrides `get()` and `post()` manually.
- Two forms in `profiles/forms.py`: `ProfileForm` (ModelForm on `Profile`, field: `phone`) and `UserUpdateForm` (ModelForm on `User`, fields: `first_name`, `last_name`).
- `UserUpdateForm` uses `get_user_model()` at module level (acceptable in forms.py, not in field definitions).
- Both forms saved in `post()` before redirecting. `messages.success()` added on save.
- URL namespace: `profiles`. Routes: `perfil/` (detail) and `perfil/editar/` (update). Included in `core/urls.py` with prefix `perfil/`.
- Templates in `templates/profiles/detail.html` and `templates/profiles/form.html`. Template variable `user_form` for `UserUpdateForm`, `form` for `ProfileForm`.
