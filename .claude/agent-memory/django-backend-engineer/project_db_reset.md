---
name: db reset on custom auth user migration
description: When AUTH_USER_MODEL changes after initial migrations, db.sqlite3 must be deleted and migrations re-run from scratch
type: project
---

If `db.sqlite3` already exists with `admin.0001_initial` applied (default Django setup) and you then introduce a custom `AUTH_USER_MODEL`, Django raises `InconsistentMigrationHistory` on `migrate`.

**Why:** The admin app's first migration depends on the auth user model. If the DB has admin migrations recorded but the custom user model migration hasn't run yet, the dependency chain is broken.

**How to apply:** On a fresh dev setup where the DB was initialized before `AUTH_USER_MODEL` was set to `users.User`, delete `db.sqlite3` and run `python manage.py migrate` again from zero.
