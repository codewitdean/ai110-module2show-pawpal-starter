from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(owner: Owner, selected_tasks: list[Task]) -> None:
    pet_by_task = {id(task): pet.name for pet in owner.pets for task in pet.tasks}

    print("Today's Schedule:\n")
    if not selected_tasks:
        print("No tasks can be scheduled within available time.")
        return

    for index, task in enumerate(selected_tasks, start=1):
        pet_name = pet_by_task.get(id(task), "Unknown Pet")
        status = "Completed" if task.completed else "Pending"
        print(
            f"{index}. {task.title} ({task.category})\n"
            f"   Pet: {pet_name}\n"
            f"   Duration: {task.duration} min\n"
            f"   Preferred time: {task.preferred_time}\n"
            f"   Priority: {task.priority}\n"
            f"   Required: {task.required}\n"
            f"   Status: {status}\n"
            f"   Notes: {task.notes}\n"
        )


if __name__ == "__main__":
    owner = Owner(name="Amina", available_minutes=90, preferences={"category": "care"})

    bella = Pet(name="Bella", species="Dog", breed="Beagle", age=4)
    luna = Pet(name="Luna", species="Cat", breed="Siamese", age=2)

    task1 = Task(
        title="Medication",
        category="care",
        duration=10,
        priority=10,
        preferred_time="09:00",
        required=True,
        notes="Give after breakfast."
    )
    task2 = Task(
        title="Morning walk",
        category="exercise",
        duration=30,
        priority=5,
        preferred_time="08:00",
        required=True,
        notes="Keep pace steady."
    )
    task3 = Task(
        title="Play session",
        category="play",
        duration=20,
        priority=7,
        preferred_time="18:00",
        recurring=True,
        frequency="daily",
        due_date=date.today(),
        notes="Use feather toy."
    )
    task4 = Task(
        title="Evening feeding",
        category="care",
        duration=15,
        priority=8,
        preferred_time="19:00",
        required=True,
        notes="Serve dinner portion."
    )

    task5 = Task(
        title="Nail trim",
        category="care",
        duration=15,
        priority=4,
        preferred_time="09:00",
        required=False,
        notes="Quick nail trim."
    )

    bella.add_task(task1)
    bella.add_task(task3)
    luna.add_task(task2)
    luna.add_task(task4)
    luna.add_task(task5)

    owner.add_pet(bella)
    owner.add_pet(luna)

    scheduler = Scheduler()

    out_of_order_tasks = [task3, task1, task4, task2]
    sorted_tasks = scheduler.sort_by_time(out_of_order_tasks)
    print("Sorted tasks by preferred time:")
    for task in sorted_tasks:
        print(f" - {task.title} at {task.preferred_time}")
    print()

    pending_tasks = scheduler.filter_tasks_by_status(owner.get_all_tasks(), completed=False)
    print("Pending tasks:")
    for task in pending_tasks:
        print(f" - {task.title} ({task.preferred_time})")
    print()

    luna_tasks = scheduler.filter_tasks_by_pet_name(owner, "Luna")
    print("Luna's tasks:")
    for task in luna_tasks:
        print(f" - {task.title} ({task.preferred_time})")
    print()

    plan = scheduler.build_daily_plan(owner)
    print_schedule(owner, plan)

    if scheduler.conflicts:
        print("\nWarnings:")
        for warning in scheduler.conflicts:
            print(f" - {warning}")

    print(scheduler.explain_plan(scheduler.selected_tasks, scheduler.skipped_tasks))

    print("\nCompleting Bella's recurring play session and creating the next occurrence...")
    next_task = scheduler.complete_task(owner, "Bella", "Play session")
    if next_task:
        print(
            f"Created next occurrence: {next_task.title} due {next_task.due_date} "
            f"at {next_task.preferred_time}"
        )
