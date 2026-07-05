"""Simple tests for PawPal+ task behavior."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pawpal_system import Pet, Priority, Task


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
