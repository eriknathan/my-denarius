---
name: users app architecture
description: Custom User model, manager, authentication backend and forms structure for the users app
type: project
---

The `users` app has a fully custom User model that removes `username` and uses `email` as the login identifier.

Key files created:
- `users/models.py` — `User(AbstractUser)` with `username=None`, `USERNAME_FIELD='email'`, `REQUIRED_FIELDS=['first_name', 'last_name']`, `created_at`/`updated_at`, custom manager `UserManager`
- `users/managers.py` — `UserManager(BaseUserManager)` with `create_user` and `create_superuser` (no username references)
- `users/backends.py` — `EmailBackend(ModelBackend)` looks up user by `email` field using `get_user_model()`
- `users/forms.py` — `UserRegistrationForm(UserCreationForm)` and `UserLoginForm(forms.Form)` with full TailwindCSS widget classes
- `users/admin.py` — custom `UserAdmin` with `ordering=['email']`, Portuguese fieldset labels, no username references
- `users/migrations/0001_initial.py` — initial migration for the custom User model

**Why:** Django's default `UserManager` references `username`; setting `username = None` without a replacement manager causes errors at migration time and in `createsuperuser`.

**How to apply:** Always use `UserManager` from `users.managers` when the custom User is involved. Never import `UserManager` from `django.contrib.auth.models`.
