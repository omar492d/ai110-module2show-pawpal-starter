"""PawPal+ domain model.

Class stubs generated from diagrams/uml_draft.mmd. No scheduling logic yet —
methods raise NotImplementedError until implemented in later steps.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum


class Priority(IntEnum):
    """Task priority. IntEnum so tasks sort naturally (HIGH first)."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    name: str
    duration_minutes: int
    priority: Priority
    category: str = ""
    preferred_time: str | None = None  # input hint: when the owner would like it
    scheduled_time: str | None = None  # output: when the scheduler placed it (None = unscheduled)
    is_recurring: bool = False
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    name: str
    age: int
    species: str
    breed: str = ""
    gender: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)

    def edit_task(self, task: Task) -> None:
        """Replace an existing task with a matching name, or add it if new."""
        for i, existing in enumerate(self.tasks):
            if existing.name == task.name:
                self.tasks[i] = task
                return
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Detach a task from this pet (no-op if it isn't attached)."""
        if task in self.tasks:
            self.tasks.remove(task)


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)


class Scheduler:
    """Stateless scheduling logic: takes a pet + a time budget, returns a plan."""

    def generate_plan(
        self, pet: Pet, available_minutes: int
    ) -> tuple[list[Task], list[Task]]:
        """Return (scheduled, skipped) for the pet's tasks — those that fit vs. those dropped.

        Tasks are considered highest-priority first; within a priority, longer
        tasks are placed first. A task is scheduled if it fits in the remaining
        budget, and its `scheduled_time` is set to its `preferred_time` when
        available. Anything that doesn't fit is skipped (and unscheduled).
        """
        ordered = sorted(
            pet.tasks,
            key=lambda t: (t.priority, t.duration_minutes),
            reverse=True,
        )

        scheduled: list[Task] = []
        skipped: list[Task] = []
        remaining = available_minutes

        for task in ordered:
            if task.duration_minutes <= remaining:
                task.scheduled_time = task.preferred_time
                remaining -= task.duration_minutes
                scheduled.append(task)
            else:
                task.scheduled_time = None
                skipped.append(task)

        return scheduled, skipped

    def explain(self, plan: tuple[list[Task], list[Task]]) -> str:
        """Explain why the given plan ordered/dropped tasks the way it did."""
        scheduled, skipped = plan
        lines = ["Scheduled (highest priority first):"]
        if scheduled:
            for task in scheduled:
                when = task.scheduled_time or "unassigned time"
                lines.append(
                    f"  - {task.name}: {task.priority.name} priority, "
                    f"{task.duration_minutes} min, at {when}"
                )
        else:
            lines.append("  (nothing fit the available time)")

        if skipped:
            lines.append("Skipped (didn't fit the time budget):")
            for task in skipped:
                lines.append(
                    f"  - {task.name}: needed {task.duration_minutes} min"
                )

        return "\n".join(lines)
