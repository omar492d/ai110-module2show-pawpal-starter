"""Simple tests for PawPal+ task behavior."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() flips a task from incomplete to complete."""
    task = Task(name="Feed", duration_minutes=10, priority=Priority.HIGH)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_count():
    """Adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Rex", age=4, species="Dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task(name="Walk", duration_minutes=30, priority=Priority.MEDIUM))

    assert len(pet.tasks) == 1


# --- Sorting correctness -------------------------------------------------


def test_sort_by_time_returns_chronological_order():
    """sort_by_time() orders scheduled tasks earliest-first by scheduled_time."""
    scheduler = Scheduler()
    noon = Task(name="Lunch", duration_minutes=10, priority=Priority.LOW,
                scheduled_time="12:00")
    morning = Task(name="Walk", duration_minutes=30, priority=Priority.HIGH,
                   scheduled_time="07:30")
    evening = Task(name="Play", duration_minutes=20, priority=Priority.LOW,
                   scheduled_time="18:30")

    ordered = scheduler.sort_by_time([noon, evening, morning])

    assert [t.scheduled_time for t in ordered] == ["07:30", "12:00", "18:30"]


def test_sort_by_time_puts_unscheduled_tasks_last():
    """Tasks with no scheduled_time sort after every scheduled task."""
    scheduler = Scheduler()
    scheduled = Task(name="Feed", duration_minutes=10, priority=Priority.HIGH,
                     scheduled_time="08:00")
    unscheduled = Task(name="Groom", duration_minutes=15, priority=Priority.LOW)

    ordered = scheduler.sort_by_time([unscheduled, scheduled])

    assert ordered == [scheduled, unscheduled]


# --- Recurrence logic ----------------------------------------------------


def test_completing_daily_task_creates_next_day_occurrence():
    """Completing a daily task adds a fresh occurrence due the following day."""
    scheduler = Scheduler()
    pet = Pet(name="Rex", age=4, species="Dog")
    today = date.today()
    walk = Task(name="Walk", duration_minutes=30, priority=Priority.HIGH,
                recurrence="daily", due_date=today, scheduled_time="07:30")
    pet.add_task(walk)

    next_task = scheduler.complete_task(pet, walk)

    # Original is marked done; a new occurrence was attached to the pet.
    assert walk.completed is True
    assert next_task is not None
    assert next_task in pet.tasks
    assert len(pet.tasks) == 2
    # The new occurrence is due tomorrow, not yet completed, and unscheduled.
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False
    assert next_task.scheduled_time is None


def test_completing_one_off_task_creates_no_new_occurrence():
    """A non-recurring task just completes; nothing new is added."""
    scheduler = Scheduler()
    pet = Pet(name="Rex", age=4, species="Dog")
    vet = Task(name="Vet visit", duration_minutes=45, priority=Priority.MEDIUM)
    pet.add_task(vet)

    next_task = scheduler.complete_task(pet, vet)

    assert next_task is None
    assert len(pet.tasks) == 1
    assert vet.completed is True


# --- Conflict detection --------------------------------------------------


def test_detect_conflicts_flags_duplicate_times():
    """Two tasks scheduled at the same time produce a conflict warning."""
    scheduler = Scheduler()
    owner = Owner(name="Omar", available_minutes=120)
    rex = Pet(name="Rex", age=4, species="Dog")
    mittens = Pet(name="Mittens", age=2, species="Cat")
    rex.add_task(Task(name="Walk", duration_minutes=30, priority=Priority.HIGH,
                      scheduled_time="08:00"))
    mittens.add_task(Task(name="Feed", duration_minutes=10, priority=Priority.HIGH,
                          scheduled_time="08:00"))
    owner.add_pet(rex)
    owner.add_pet(mittens)

    warnings = scheduler.detect_conflicts(owner)

    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_detect_conflicts_no_warning_for_distinct_times():
    """Tasks at different times, and unscheduled tasks, raise no conflict."""
    scheduler = Scheduler()
    owner = Owner(name="Omar", available_minutes=120)
    rex = Pet(name="Rex", age=4, species="Dog")
    rex.add_task(Task(name="Walk", duration_minutes=30, priority=Priority.HIGH,
                      scheduled_time="08:00"))
    rex.add_task(Task(name="Play", duration_minutes=20, priority=Priority.LOW,
                      scheduled_time="18:00"))
    # Unscheduled task shares no slot and must never conflict.
    rex.add_task(Task(name="Groom", duration_minutes=15, priority=Priority.LOW))
    owner.add_pet(rex)

    assert scheduler.detect_conflicts(owner) == []


# --- Filtering logic -----------------------------------------------------


def test_filter_tasks_narrows_by_pet_and_completion():
    """filter_tasks() narrows by pet_name and completion; None skips a filter."""
    owner = Owner(name="Omar", available_minutes=120)
    rex = Pet(name="Rex", age=4, species="Dog")
    mittens = Pet(name="Mittens", age=2, species="Cat")
    rex.add_task(Task(name="Walk", duration_minutes=30, priority=Priority.HIGH,
                      completed=True))
    rex.add_task(Task(name="Play", duration_minutes=20, priority=Priority.LOW))
    mittens.add_task(Task(name="Feed", duration_minutes=10, priority=Priority.HIGH))
    owner.add_pet(rex)
    owner.add_pet(mittens)

    # No filters: every task across all pets.
    assert len(owner.filter_tasks()) == 3
    # By pet only.
    assert {t.name for t in owner.filter_tasks(pet_name="Rex")} == {"Walk", "Play"}
    # By completion only.
    assert [t.name for t in owner.filter_tasks(completed=True)] == ["Walk"]
    # Both filters combined.
    assert [t.name for t in owner.filter_tasks(pet_name="Rex", completed=False)] == ["Play"]
