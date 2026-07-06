# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
============================================
Today's Schedule for Omar
============================================
07:30  Rex      Morning walk (30 min, HIGH)
08:00  Rex      Give medication (5 min, HIGH)
08:00  Mittens  Feed breakfast (10 min, HIGH)
14:00  Rex      Vet checkup (45 min, MEDIUM)
18:30  Mittens  Playtime (20 min, LOW)
============================================

All scheduled tasks, in the order they were added:
  07:30  Morning walk
  08:00  Give medication
  14:00  Vet checkup
  08:00  Feed breakfast
  18:30  Playtime

Same tasks after Scheduler.sort_by_time():
  07:30  Morning walk
  08:00  Give medication
  08:00  Feed breakfast
  14:00  Vet checkup
  18:30  Playtime

filter_tasks(completed=False)  -> still to do:
  Morning walk
  Give medication
  Playtime

filter_tasks(completed=True)   -> already done:
  Vet checkup
  Feed breakfast

filter_tasks(pet_name='Rex')   -> all of Rex's tasks:
  Vet checkup (done)
  Morning walk (pending)
  Give medication (pending)

Conflict check:
  ⚠️  Conflict at 08:00: Rex's 'Give medication', Mittens's 'Feed breakfast' are all scheduled together.
```

## 🧪 Testing PawPal+
The tests in tests/test_pawpal.py verify the program's core behaviors: marking tasks complete, adding tasks to pets, sorting tasks chronologically, spawning next-day occurrences for recurring tasks, and flagging scheduling conflicts at duplicate time slots.

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
====================================================================================== test session starts =======================================================================================
platform darwin -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/omard./Downloads/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 9 items                                                  

tests/test_pawpal.py .........                                                 [100%]

======================================================================================= 9 passed in 0.02s ========================================================================================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.generate_plan`, `Scheduler.sort_by_time` | By priority/duration, or by time |
| Filtering | `Scheduler.generate_plan`, `Owner.filter_tasks` | Skips over-budget tasks; filters by status/pet |
| Conflict handling | `Scheduler.detect_conflicts` | Warns on shared time slots |
| Recurring tasks | `Task.mark_complete`, `Scheduler.complete_task` | Spawns next daily/weekly occurrence |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. In the **sidebar**, set the **owner name** and the **available minutes** for the day (this is the time budget the scheduler fits tasks into).
2. Still in the sidebar, use the **Add a pet** form to enter the pet's name, species, age, gender, and breed, then click **Add pet**. The pet becomes active and its details appear as a header in the main area.
3. On the **📋 Tasks** tab, add tasks one at a time: enter a title, duration, priority (low/medium/high), preferred time (`HH:MM`), and whether it **repeats** (one-off/daily/weekly), then click **Add task**. Each task appears in the task list below.
4. Manage tasks from the list: check a task off to mark it **complete** (a recurring task automatically spawns its next occurrence), remove one with the **🗑️** button, or narrow the view with the **All / Pending / Completed** filter.
5. On the **🗓️ Schedule** tab, click **Generate schedule** to run the scheduler across all pets — it fits tasks into the budget priority-first, then sorts them chronologically into today's plan.
6. Review the results. The app shows today's schedule for tasks that were successfully scheduled, displays the tasks that do not fit the time budget, warns the user in case of a time conflict, and provides a simple explanation for the selected plan.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here --> 