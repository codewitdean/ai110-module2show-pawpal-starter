import pytest

from pawpal_system import Owner, Pet, Task


def test_task_mark_complete_changes_status():
    task = Task(
        title="Medication",
        category="care",
        duration=10,
        priority=10,
        preferred_time="09:00",
        required=True,
        notes="Give after breakfast.",
    )

    assert not task.completed
    task.mark_complete()
    assert task.completed


def test_pet_add_task_increases_task_count():
    pet = Pet(name="Bella", species="Dog", breed="Beagle", age=4)
    assert len(pet.tasks) == 0

    task = Task(
        title="Morning walk",
        category="exercise",
        duration=20,
        priority=8,
        preferred_time="08:00",
    )

    pet.add_task(task)
    assert len(pet.tasks) == 1
    assert pet.tasks[0].title == "Morning walk"
