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
        title="Morning walk",
        category="exercise",
        duration=30,
        priority=5,
        preferred_time="08:00",
        required=True,
        notes="Keep pace steady."
    )
    task2 = Task(
        title="Medication",
        category="care",
        duration=10,
        priority=10,
        preferred_time="09:00",
        required=True,
        notes="Give after breakfast."
    )
    task3 = Task(
        title="Play session",
        category="play",
        duration=20,
        priority=7,
        preferred_time="18:00",
        recurring=True,
        notes="Use feather toy."
    )

    bella.add_task(task1)
    bella.add_task(task2)
    luna.add_task(task3)

    owner.add_pet(bella)
    owner.add_pet(luna)

    scheduler = Scheduler()
    plan = scheduler.build_daily_plan(owner)

    print_schedule(owner, plan)
    print(scheduler.explain_plan(scheduler.selected_tasks, scheduler.skipped_tasks))
