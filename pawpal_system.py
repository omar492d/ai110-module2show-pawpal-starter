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
    preferred_time: str | None = None
    is_recurring: bool = False
    completed: bool = False


@dataclass
class Pet:
    name: str
    age: int
    species: str
    breed: str = ""
    gender: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def edit_task(self, task: Task) -> None:
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        raise NotImplementedError


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError


@dataclass
class ScheduledTask:
    """A task assigned a concrete start time in a generated plan."""

    task: Task
    start_time: str


class Scheduler:
    """Stateless scheduling logic: takes tasks + a time budget, returns a plan."""

    def generate_plan(
        self, tasks: list[Task], available_minutes: int
    ) -> tuple[list[ScheduledTask], list[Task]]:
        """Return (scheduled, skipped) — tasks that fit vs. those dropped."""
        raise NotImplementedError

    def explain(self) -> str:
        """Explain why the plan ordered/dropped tasks the way it did."""
        raise NotImplementedError
