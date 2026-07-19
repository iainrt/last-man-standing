# Football Data Synchronisation

This document explains how football data is imported from API-Football.

---

# Overview

The application imports football data using a series of Django management commands.

These commands should normally be run in the order shown below.

---

# Step 1 — Sync Leagues

Imports supported leagues.

```bash
uv run python manage.py sync_leagues
```

---

# Step 2 — Sync Seasons

Imports available seasons.

```bash
uv run python manage.py sync_seasons
```

---

# Step 3 — Sync Teams

Imports all teams for the configured league and season.

```bash
uv run python manage.py sync_teams
```

---

# Step 4 — Sync Gameweeks

Creates gameweeks for the season.

```bash
uv run python manage.py sync_gameweeks
```

---

# Step 5 — Sync Fixtures

Imports fixtures for every gameweek.

```bash
uv run python manage.py sync_fixtures
```

---

# Typical New Season Workflow

When starting a brand new football season:

Run:

```bash
sync_leagues

sync_seasons

sync_teams

sync_gameweeks

sync_fixtures
```

in that order.

---

# During the Season

Fixtures and results should be synchronised regularly.

Typically:

```bash
uv run python manage.py sync_fixtures
```

will update:

- fixture times
- match status
- scores
- results

---

# Result Processing

Once completed fixtures have been synchronised:

```bash
uv run python manage.py process_results
```

This command:

- updates selections
- awards achievements
- eliminates players
- evaluates competition winners
- creates notifications

---

# Running Against Production

Use the production management script.

Example:

```bash
./scripts/production_manage.sh sync_fixtures

./scripts/production_manage.sh process_results
```

---

# Notes

The synchronisation commands are designed to be idempotent.

Running them multiple times should update existing records rather than creating duplicates.