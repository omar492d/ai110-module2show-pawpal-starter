"""PawPal+ demo: build an owner with pets and tasks, then print today's schedule."""

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def build_owner() -> Owner:
    """Create an owner, add two pets, and give each pet some tasks."""
    owner = Owner(name="Omar", available_minutes=90)

    rex = Pet(name="Rex", age=4, species="Dog", breed="Labrador", gender="M")
    mittens = Pet(name="Mittens", age=2, species="Cat", breed="Tabby", gender="F")

    owner.add_pet(rex)
    owner.add_pet(mittens)

    # At least three tasks, each with a different preferred time.
    rex.add_task(
        Task(
            name="Morning walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            category="Exercise",
            preferred_time="07:30",
        )
    )
    rex.add_task(
        Task(
            name="Vet checkup",
            duration_minutes=45,
            priority=Priority.MEDIUM,
            category="Health",
            preferred_time="14:00",
        )
    )
    mittens.add_task(
        Task(
            name="Feed breakfast",
            duration_minutes=10,
            priority=Priority.HIGH,
            category="Feeding",
            preferred_time="08:00",
        )
    )
    mittens.add_task(
        Task(
            name="Playtime",
            duration_minutes=20,
            priority=Priority.LOW,
            category="Enrichment",
            preferred_time="18:30",
        )
    )

    return owner


def print_todays_schedule(owner: Owner) -> None:
    """Run the scheduler for each pet and print an ordered daily schedule."""
    scheduler = Scheduler()

    entries: list[tuple[str, str, Task]] = []
    for pet in owner.pets:
        scheduled, _skipped = scheduler.generate_plan(pet, owner.available_minutes)
        for task in scheduled:
            when = task.scheduled_time or "--:--"
            entries.append((when, pet.name, task))

    entries.sort(key=lambda e: e[0])

    print("=" * 44)
    print(f"Today's Schedule for {owner.name}")
    print("=" * 44)
    for when, pet_name, task in entries:
        print(
            f"{when}  {pet_name:<8} {task.name} "
            f"({task.duration_minutes} min, {task.priority.name})"
        )
    print("=" * 44)


if __name__ == "__main__":
    print_todays_schedule(build_owner())
