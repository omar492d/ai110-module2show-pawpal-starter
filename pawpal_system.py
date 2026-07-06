from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from enum import IntEnum


# How far ahead the next occurrence lands, per recurrence rule.
RECURRENCE_STEPS: dict[str, timedelta] = {
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1),  # timedelta(weeks=1) == timedelta(days=7)
}


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
    recurrence: str | None = None  # "daily", "weekly", or None for a one-off task
    due_date: date | None = None  # the day this occurrence is due
    completed: bool = False

    def next_occurrence(self) -> Task | None:
        """Return a fresh copy due one recurrence step later, or None if it's a one-off."""
        step = RECURRENCE_STEPS.get((self.recurrence or "").lower())
        if step is None:
            return None
        base = self.due_date or date.today()
        return replace(
            self,
            due_date=base + step,
            completed=False,
            scheduled_time=None,
        )

    def mark_complete(self) -> Task | None:
        """Mark this task done; if it recurs, return the next occurrence to schedule."""
        self.completed = True
        return self.next_occurrence()


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

    def filter_tasks(
        self,
        *,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Return tasks across all pets, narrowed by completion status and/or pet name (None skips a filter)."""
        results: list[Task] = []
        for pet in self.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                results.append(task)
        return results


class Scheduler:
    """Stateless scheduling logic: takes a pet + a time budget, returns a plan."""

    def generate_plan(
        self, pet: Pet, available_minutes: int
    ) -> tuple[list[Task], list[Task]]:
        """Fit the pet's tasks into the time budget (priority first); return (scheduled, skipped)."""
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

    def complete_task(self, pet: Pet, task: Task) -> Task | None:
        """Mark a task complete, auto-add its next occurrence to the pet if it recurs, and return it (or None)."""
        next_task = task.mark_complete()
        if next_task is not None:
            pet.add_task(next_task)
        return next_task

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by scheduled_time ("HH:MM"); unscheduled tasks last."""
        return sorted(
            tasks,
            key=lambda t: t.scheduled_time or "99:99",
        )

    def detect_conflicts(self, owner: Owner) -> list[str]:
        """Return a warning per time slot shared by 2+ scheduled tasks (same- or cross-pet); empty if none."""
        by_time: dict[str, list[tuple[str, Task]]] = {}
        for pet in owner.pets:
            for task in pet.tasks:
                if task.scheduled_time is None:
                    continue  # unscheduled tasks can't clash
                by_time.setdefault(task.scheduled_time, []).append((pet.name, task))

        warnings: list[str] = []
        for when in sorted(by_time):
            clashing = by_time[when]
            if len(clashing) > 1:
                who = ", ".join(f"{pet_name}'s '{task.name}'" for pet_name, task in clashing)
                warnings.append(f"Conflict at {when}: {who} are all scheduled together.")
        return warnings

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
