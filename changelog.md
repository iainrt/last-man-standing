# Changelog

All notable changes to this project are documented in this file.

The format is inspired by *Keep a Changelog* and the project follows Semantic Versioning where practical.

---

## Version 0.9 (Closed Alpha)

**Release Date:** TBC

### Added

* Achievement system with visible and Discovery achievements.
* Achievement XP rewards and progress tracking.
* Achievement notifications with persistent dismissible alerts.
* Public player profiles with configurable privacy settings.
* Public achievement showcase with protection for locked Discovery achievements.
* Comprehensive player statistics including:

  * Competitions entered
  * Competitions completed
  * Competitions won
  * Competitions currently alive
  * Competition win percentage
  * Successful picks
  * Eliminated picks
  * Weeks survived
  * Joker uses
  * Joker saves
  * Unique clubs picked
  * Favourite club
* Rarest achievement calculation based on active players.
* Competition Winner and Joint Winner achievements.
* Internal achievement checking service architecture.
* Release documentation, test plan and known issues documentation.

### Changed

* Improved competition result processing workflow.
* Added gameweek result processing tracking to prevent duplicate processing.
* Improved login error message visibility.
* Improved public profile and achievement presentation.
* Refactored player statistics into a dedicated statistics service.
* Refactored achievement processing into modular checker services.

### Fixed

* Players who fail to submit a selection before the gameweek deadline are now eliminated correctly.
* Prevented duplicate processing of completed competition gameweeks.
* Fixed several achievement notification and display issues.
* Improved overall application stability and reliability.

### Internal

* Expanded project documentation.
* Added structured release notes.
* Added formal regression test plan.
* Continued improvements to project architecture and code organisation.

---

## Version 0.8 (Early Access)

*(Existing v0.8 changelog remains below this point.)*


# Version 0.8 Early Access

## Features

- Last Man Standing competitions
- Joker support
- Competition admins
- Automatic fixture updates
- Automatic result processing
- Winner detection
- Pick popularity
- Survivor leaderboard

## Known limitations

- Tailwind Play CDN (proper build planned for v1.0)
- Achievements coming in v0.9