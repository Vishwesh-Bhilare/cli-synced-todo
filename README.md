# CLI ToDo List

A cross-platform, plain-text todo system using **Markdown** and a **single script**.
Designed to work cleanly across **Linux, Windows and Android** with file sync (Drive, Syncthing, etc.).
No apps, no lock-in, no database.

---

## Goals

* Human-readable plain text
* Cross-platform editing
* Scripted recurrence handling
* Clean separation of active vs completed tasks
* Infinite grouping using Markdown headings

---

## Folder Structure

```
todos/
├── todo.md        # Active tasks (synced)
├── done.md        # Completed tasks, grouped by day (synced)
├── rollover.py    # Task processing script
└── README.md      # Documentation (this file)
```

Only `todo.md` and `done.md` need syncing.

---

## Core Concepts

### 1. Tasks

* One task per line
* Markdown checkbox syntax
* Metadata is inline

```
- [ ] Example task
- [x] Completed task
```

---

### 2. Grouping (including nested groups)

Grouping is done using **Markdown headings**.

Heading depth = group depth.

```
# College
## Math
### Algebra
- [ ] Revise chapters

## Physics
- [ ] Lab report
```

Tasks belong to the nearest heading above them.

No limits on nesting.

---

### 3. Metadata Format

Metadata is written as `key:value` at the end of the task line.

Supported fields:

| Field    | Format       | Description     |
| -------- | ------------ | --------------- |
| `due`    | `DD-MM-YYYY` | Due date        |
| `repeat` | see below    | Recurrence rule |

Example:

```
- [ ] Submit assignment due:08-01-2026 repeat:weekly
```

---

## Recurrence Rules

### Fixed intervals

```
repeat:daily
repeat:weekly
repeat:monthly
repeat:yearly
```

### Weekday-based

```
repeat:mon,wed,fri
repeat:tue,thu
```

Valid weekday values:

```
mon tue wed thu fri sat sun
```

---

## Files Explained

### `todo.md`

* Contains **only active tasks**
* Tasks are grouped by headings
* Completed tasks are removed automatically

Example:

```md
# College
## CS
- [ ] DSA practice repeat:mon,wed,fri
- [ ] Assignment due:10-01-2026

# Personal
- [ ] Gym repeat:mon,wed,fri
```

---

### `done.md`

* Permanent history log
* Grouped by **completion date**
* Tasks appear under the day they were completed

Example:

```md
# 07-01-2026
- [x] Gym repeat:mon,wed,fri
- [x] DSA practice repeat:mon,wed,fri

# 08-01-2026
- [x] Assignment due:08-01-2026
```

---

## Script Behavior (`rollover.py`)

When run:

1. Scans `todo.md`
2. Finds completed tasks (`- [x]`)
3. Moves them to `done.md` under today’s date
4. If the task has `repeat:`:

   * Computes the next due date
   * Recreates the task as unchecked in `todo.md`

### Important notes

* Completion date = script run date
* Group structure in `todo.md` is preserved
* Reinserted repeating tasks are appended at the end
* Script has no background execution

---

## Usage

### Mark tasks complete

Edit `todo.md` and change:

```
- [ ] Task
```

to:

```
- [x] Task
```

### Process tasks

Run:

```bash
python rollover.py
```

This updates both files.

---

## Platform Workflow

### Linux

* Edit with any editor
* Run the script manually or via cron/systemd

### Android

* Edit `todo.md` using any Markdown editor
* Do **not** run the script on Android
* Sync handles propagation

---

## Rules You Must Follow

* One task per line
* Metadata must be lowercase
* Dates must be `DD-MM-YYYY`
* Do not split tasks across lines
* Do not put tasks above headings

Breaking these rules will break automation.

---

## Design Philosophy

* Plain text over apps
* Explicit structure over magic
* Scripts over services
* Files you can read in 10 years

---

## Extending the System

Safe extensions:

* `priority:A`
* `completed:DD-MM-YYYY`
* CLI views (`today`, `week`)
* Lua port of the script
* Sorting by due date

Do **not** add hidden state or databases.

---

## License

Public domain.
Use it, fork it, adapt it.

---

## Final Note

If this system ever feels limiting, the problem is not the format —
it’s the discipline.

Text scales.