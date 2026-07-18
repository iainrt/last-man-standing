# Release Checklist

This document describes the standard release process for deploying a new version of Last Man Standing.

The aim is to ensure every release follows the same repeatable process and that no deployment steps are missed.

---

# 1. Development Complete

- [ ] All planned features have been completed.
- [ ] Feature branches have been merged into the release branch.
- [ ] Code review completed.
- [ ] Documentation updated.
- [ ] CHANGELOG.md updated.
- [ ] Release notes written.
- [ ] Known issues documented.

---

# 2. Testing

## Developer Testing

- [ ] Complete the release test plan.
- [ ] Confirm all previous bugs remain fixed.
- [ ] Confirm no new regressions have been introduced.

## Smoke Tests

- [ ] Registration.
- [ ] Login.
- [ ] Profile editing.
- [ ] Competition creation.
- [ ] Competition joining.
- [ ] Selection submission.
- [ ] Result processing.
- [ ] Achievements.
- [ ] Public profiles.

---

# 3. Git

## Merge Bug Fixes

Merge any remaining bug fix branches into the release branch.

Example:

```bash
git checkout release/vX.X
git pull
git merge bugs/vX.X-fixes
git push
```

## Pull Request

Create a Pull Request:

```
release/vX.X → main
```

Review all changed files before merging.

---

# 4. Production Deployment

Merge the Pull Request.

Confirm that Vercel successfully deploys the latest version.

Verify:

- [ ] Deployment successful.
- [ ] No deployment errors.
- [ ] Site loads correctly.

---

# 5. Production Database

Run all required production commands using the production management script.

## Check Configuration

```bash
./scripts/production_manage.sh check
```

- [ ] Completed

---

## Apply Migrations

```bash
./scripts/production_manage.sh migrate
```

- [ ] Completed

---

## Seed Reference Data

Run any required seed commands.

Example:

```bash
./scripts/production_manage.sh seed_achievements
```

- [ ] Completed

---

## Verify Migrations

```bash
./scripts/production_manage.sh showmigrations
```

- [ ] All migrations applied

---

# 6. Production Smoke Test

Verify the live site.

## Accounts

- [ ] Login
- [ ] Logout
- [ ] Register
- [ ] Profile update

## Competitions

- [ ] Competition loads
- [ ] Competition creation
- [ ] Join competition
- [ ] Make selection

## Achievements

- [ ] Achievement page loads
- [ ] Notifications work
- [ ] XP displays correctly

## Profiles

- [ ] Public profile
- [ ] Statistics
- [ ] Achievement visibility

## Administration

- [ ] Django admin accessible
- [ ] Management commands functioning

---

# 7. Closed Alpha / Production Monitoring

Following release:

- [ ] Monitor application logs.
- [ ] Monitor Supabase.
- [ ] Monitor GitHub Issues.
- [ ] Record tester feedback.
- [ ] Prioritise new issues.

---

# 8. Release Complete

- [ ] Version tag created.
- [ ] GitHub Release published (optional).
- [ ] Documentation committed.
- [ ] Backup completed (if required).

---

# Rollback Plan

If a critical issue is discovered:

1. Disable affected functionality if possible.
2. Investigate logs.
3. Fix on a bug fix branch.
4. Test the fix locally.
5. Merge into the release branch.
6. Create a Pull Request to `main`.
7. Redeploy.
8. Re-run production migrations if required.

---

# Release History

| Version | Status | Date |
|----------|--------|------|
| v0.8 | Early Access | Completed |
| v0.9 | Closed Alpha | |
| v1.0 | Public Release | |