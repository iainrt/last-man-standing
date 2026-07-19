# Achievement System Design

**Project:** Last Man Standing  
**Version:** Draft for v0.9 Early Access  
**Status:** Living Design Document

---

# 1. Purpose

The achievement system exists to reward player progression, encourage long-term engagement and create community discussion.

Unlike simple badges, achievements form the foundation of the wider Player Progression System which will eventually include:

- Achievements
- XP
- Levels
- Prestige
- Statistics
- Elo
- Cosmetics

The system is designed so that new achievements can be released throughout each season without requiring changes to the underlying architecture.

---

# 2. Design Principles

The achievement system follows these principles:

1. Reward progress as well as completion.
2. Hidden achievements should encourage community discussion.
3. New achievements should be released regularly throughout the season.
4. Achievements should feel meaningful rather than repetitive.
5. All unlocks pass through a single achievement service.
6. Player progression should integrate naturally with XP and Levels.
7. Public player profiles should encourage comparison while respecting privacy.
8. Achievement logic should be separated from gameplay logic.

---

# 3. Architecture

```
Player Action
      │
      ▼
Game Logic
      │
      ▼
Achievement Checker
      │
      ▼
Achievement Service
      │
      ▼
Progress Updated
      │
      ▼
Achievement Unlocked
      │
      ▼
Player Notification
      │
      ▼
Public Profile / Catalogue
```

Gameplay never writes directly to UserAchievement.

All achievement updates must pass through the Achievement Service.

---

# 4. Database Design

## Achievement

Represents a single achievement definition.

### Fields

- code
- name
- description
- discovery
- category
- difficulty
- icon
- xp_reward
- target
- tracking_start
- display_order
- is_active
- created_at

Achievement definitions are seeded via the management command and are not created manually.

---

## UserAchievement

Represents one player's progress towards an achievement.

### Fields

- user
- achievement
- progress
- is_unlocked
- unlocked_at
- created_at
- updated_at

Progress is cumulative.

Completion occurs automatically once progress reaches the configured target.

---

# 5. Unlock Architecture

Achievement logic is split by game event.

```
services/

unlock_service.py

checkers/

selection.py

result.py

competition.py

collection.py

statistics.py
```

## Selection

Triggered whenever a player submits or edits a pick.

Examples:

- First Pick
- Joker Played

---

## Result

Triggered after fixture processing.

Examples:

- Week One Survivor
- Joker Saved Me

---

## Competition

Triggered when a competition ends.

Examples:

- Competition Winner
- Joint Winner

---

## Collection

Future achievements based on collecting clubs.

Examples:

- All 92 Clubs
- Welsh Wanderer
- Yorkshire Tripper

---

## Statistics

Future achievements based on player statistics.

Examples:

- Against the Crowd
- Popular Choice
- Perfect Start

---

# 6. Achievement Discovery

Achievements have two discovery types.

## Visible

Displayed from the beginning.

Players can always view:

- name
- description
- progress
- reward

---

## Hidden

Before unlocking:

Display only:

- mystery icon
- clue
- anonymous progress bar

Do NOT display:

- achievement name
- achievement description
- numeric progress
- target value

After unlocking the achievement behaves exactly like a visible achievement.

---

# 7. Hidden Achievement Rules

Hidden achievements exist to promote discussion within the community.

Players should never be able to discover hidden achievement details simply by viewing another player's profile.

Rule:

A hidden achievement is only revealed if:

- the current player has unlocked it

OR

- it is their own profile

Otherwise the mystery presentation remains.

---

# 8. Achievement Categories

Current categories

- Milestone
- Competition
- Picks
- Joker
- Collection
- Exploration
- Special

Future categories

- Seasonal
- Community
- Legendary

---

# 9. Difficulty Levels

Current difficulties

- Bronze
- Silver
- Gold
- Platinum
- Legendary

Difficulty influences:

- card styling
- rarity
- XP reward

Difficulty does not affect unlock logic.

---

# 10. Progress Tracking

Every achievement defines a target value.

Examples

| Achievement | Target |
|------------|-------:|
| First Pick | 1 |
| Joker Played | 1 |
| Week One Survivor | 1 |
| Perfect Start | 3 |
| All 92 Clubs | 92 |

Progress is stored even when the achievement has not yet been unlocked.

---

# 11. Tracking Start

Every achievement has a tracking_start field.

Only activity occurring on or after this date contributes towards progress.

Purpose:

- new achievements can be introduced mid-season
- players do not receive achievements retrospectively
- seasonal releases remain meaningful

---

# 12. Achievement Catalogue

The catalogue is the master view of all achievements.

Features:

- summary card
- progress bars
- hidden achievements
- completed achievements
- XP earned

Future additions:

- filters
- search
- rarity
- newest achievements
- seasonal achievements

---

# 13. Public Profiles

Player profiles will eventually include:

- favourite club
- achievements
- statistics
- level
- prestige
- XP
- Elo

Players may choose whether their profile is public.

Screen names throughout the application link to the player's public profile.

---

# 14. Notifications

When an achievement unlocks the player should receive immediate feedback.

v0.9

- Django success message

Future

- toast notification
- animation
- sound
- activity feed

---

# 15. XP Integration

Achievements award XP.

XP contributes towards:

```
Achievements
      │
      ▼
XP
      │
      ▼
Levels
      │
      ▼
Prestige
```

The XP system is planned for v1.0.

---

# 16. Community Features

Planned additions

- percentage of players who have unlocked an achievement
- recently unlocked achievements
- rarest achievements
- seasonal achievement releases
- community discussion

---

# 17. Future Achievement Ideas

Examples

- Competition Winner
- Perfect Start
- Joker Saved Me
- Against the Crowd
- Popular Choice
- All 92 Clubs
- Welsh Wanderer
- Yorkshire Tripper
- Pick every Championship club
- Pick every League One club
- Pick every League Two club
- Hat-trick Hero
- Five Goal Thriller
- 90th Minute Winner
- Cup Specialist
- Boxing Day Survivor

This list is intentionally non-exhaustive and will continue to expand.

---

# 18. Release Strategy

Achievements should be released gradually.

Proposed cadence:

- Major release before each season.
- One or two achievement drops during the season.
- Seasonal achievements retired and replaced where appropriate.

Regular additions keep the game feeling fresh without changing core gameplay.

---

# 19. Long-Term Vision

The achievement system should become one of the defining features of Last Man Standing.

Players should be encouraged to:

- compare achievements
- complete collections
- discover hidden achievements
- progress through levels
- build long-term player identity

The achievement system forms the foundation of the wider Player Progression System and is intended to evolve throughout the lifetime of the project.