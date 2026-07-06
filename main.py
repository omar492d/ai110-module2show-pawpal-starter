"""PawPal+ demo: build an owner with pets and tasks, then print today's schedule."""

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def build_owner() -> Owner:
    """Create an owner, add two pets, and give each pet some tasks."""
    owner = Owner(name="Omar", available_minutes=90)

    rex = Pet(name="Rex", age=4, species="Dog", breed="Labrador", gender="M")
    mittens = Pet(name="Mittens", age=2, species="Cat", breed="Tabby", gender="F")

    owner.add_pet(rex)
    owner.add_pet(mittens)

    # Tasks are added out of chronological order on purpose, so the
    # sort_by_time demo below has something real to reorder.
    rex.add_task(
        Task(
            name="Vet checkup",
            duration_minutes=45,
            priority=Priority.MEDIUM,
            category="Health",
            preferred_time="14:00",
        )
    )
    rex.add_task(
        Task(
            name="Morning walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            category="Exercise",
            preferred_time="07:30",
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
    mittens.add_task(
        Task(
            name="Feed breakfast",
            duration_minutes=10,
            priority=Priority.HIGH,
            category="Feeding",
            preferred_time="08:00",
        )
    )
    # Deliberate clash: Rex needs meds at 08:00, the same slot as Mittens'
    # breakfast above -> a cross-pet conflict for detect_conflicts to catch.
    rex.add_task(
        Task(
            name="Give medication",
            duration_minutes=5,
            priority=Priority.HIGH,
            category="Health",
            preferred_time="08:00",
        )
    )

    # Mark a couple of tasks done so the completion filter has both sides.
    rex.tasks[0].mark_complete()      # Vet checkup
    mittens.tasks[1].mark_complete()  # Feed breakfast

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


def demo_sorting(owner: Owner) -> None:
    """Show Scheduler.sort_by_time reordering tasks that were added out of order."""
    scheduler = Scheduler()

    # Give tasks a scheduled_time to sort by (the scheduler copies preferred_time).
    all_tasks: list[Task] = []
    for pet in owner.pets:
        scheduled, _skipped = scheduler.generate_plan(pet, owner.available_minutes)
        all_tasks.extend(scheduled)

    print("\nAll scheduled tasks, in the order they were added:")
    for task in all_tasks:
        print(f"  {task.scheduled_time}  {task.name}")

    print("\nSame tasks after Scheduler.sort_by_time():")
    for task in scheduler.sort_by_time(all_tasks):
        print(f"  {task.scheduled_time}  {task.name}")


def demo_filtering(owner: Owner) -> None:
    """Show Owner.filter_tasks narrowing by completion status and by pet name."""
    print("\nfilter_tasks(completed=False)  -> still to do:")
    for task in owner.filter_tasks(completed=False):
        print(f"  {task.name}")

    print("\nfilter_tasks(completed=True)   -> already done:")
    for task in owner.filter_tasks(completed=True):
        print(f"  {task.name}")

    print("\nfilter_tasks(pet_name='Rex')   -> all of Rex's tasks:")
    for task in owner.filter_tasks(pet_name="Rex"):
        status = "done" if task.completed else "pending"
        print(f"  {task.name} ({status})")


def demo_conflicts(owner: Owner) -> None:
    """Schedule every pet, then show Scheduler.detect_conflicts warning on clashes."""
    scheduler = Scheduler()
    for pet in owner.pets:
        scheduler.generate_plan(pet, owner.available_minutes)

    print("\nConflict check:")
    warnings = scheduler.detect_conflicts(owner)
    if warnings:
        for warning in warnings:
            print(f"  ⚠️  {warning}")
    else:
        print("  No conflicts — every task has its own time slot.")


if __name__ == "__main__":
    owner = build_owner()
    print_todays_schedule(owner)
    demo_sorting(owner)
    demo_filtering(owner)
    demo_conflicts(owner)
