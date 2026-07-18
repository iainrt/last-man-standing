# Development Workflow

This document explains how to run Django management commands against the development and production databases.

---

# Overview

The project uses two separate Supabase databases:

- Development
- Production

To reduce the risk of accidental changes, separate scripts are used for each environment.

---

# Development Commands

Development commands always use the local `.env` file.

Example:

```bash
uv run python manage.py migrate
```

Other common commands:

```bash
uv run python manage.py runserver

uv run python manage.py makemigrations

uv run python manage.py createsuperuser

uv run python manage.py shell

uv run python manage.py check
```

---

# Production Commands

Never execute production commands directly.

Instead use:

```bash
./scripts/production_manage.sh <command>
```

The script:

- loads `.env.production`
- asks for confirmation
- runs the Django management command

Example:

```bash
./scripts/production_manage.sh migrate
```

---

# Common Production Commands

Check configuration

```bash
./scripts/production_manage.sh check
```

Apply migrations

```bash
./scripts/production_manage.sh migrate
```

Seed achievements

```bash
./scripts/production_manage.sh seed_achievements
```

Show migrations

```bash
./scripts/production_manage.sh showmigrations
```

Open Django shell

```bash
./scripts/production_manage.sh shell
```

---

# Typical Release Process

1. Merge release branch into `main`
2. Vercel deploys the latest code
3. Run production migrations

```bash
./scripts/production_manage.sh migrate
```

4. Seed achievements

```bash
./scripts/production_manage.sh seed_achievements
```

5. Verify the deployment.

---

# Warning

Never point your local development environment at the production database.

Always use the production management script when working with the production environment.