from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


Preferences = Dict[str, str]


@dataclass
class Task:
    title: str
    category: str
    duration: int
    priority: int
    preferred_time: str
    required: bool = False
    recurring: bool = False
    completed: bool = False
    notes: str = ""

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.completed = False

    def update_priority(self, priority: int) -> None:
        """Update the priority level for this task."""
        self.priority = priority

    def matches_preference(self, preferences: Preferences) -> bool:
        """Return True if this task matches the given preferences."""
        if not preferences:
            return True

        if "category" in preferences and self.category != preferences["category"]:
            return False

        if "preferred_time" in preferences and self.preferred_time != preferences["preferred_time"]:
            return False

        return True


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task_title: str) -> None:
        """Remove a task by title from this pet."""
        self.tasks = [task for task in self.tasks if task.title != task_title]

    def edit_task(self, task_title: str, updated_task: Task) -> None:
        """Replace an existing task with updated task details."""
        for index, task in enumerate(self.tasks):
            if task.title == task_title:
                self.tasks[index] = updated_task
                break

    def get_tasks(self) -> List[Task]:
        """Return a copy of this pet's task list."""
        return list(self.tasks)


class Owner:
    def __init__(
        self,
        name: str,
        available_minutes: int = 0,
        preferences: Optional[Preferences] = None,
    ):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name from this owner."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Return the pet with the given name, or None if not found."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def update_available_time(self, minutes: int) -> None:
        """Update how many minutes the owner has available."""
        self.available_minutes = minutes

    def set_preference(self, key: str, value: str) -> None:
        """Set a scheduling preference for the owner."""
        self.preferences[key] = value

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across every pet owned by this owner."""
        return [task for pet in self.pets for task in pet.get_tasks()]


class Scheduler:
    def __init__(self, owner: Optional[Owner] = None) -> None:
        """Initialize the scheduler, optionally with an owner."""
        self.owner = owner
        self.selected_tasks: List[Task] = []
        self.skipped_tasks: List[Task] = []
        self.total_time_used: int = 0

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by requirement, priority, and duration."""
        return sorted(
            tasks,
            key=lambda task: (
                not task.required,
                -task.priority,
                task.duration,
            ),
        )

    def build_daily_plan(self, owner: Owner) -> List[Task]:
        """Build a daily task schedule for the given owner."""
        self.owner = owner
        tasks = owner.get_all_tasks()
        available_minutes = owner.available_minutes
        self.selected_tasks = []
        self.skipped_tasks = []
        self.total_time_used = 0

        for task in self.sort_tasks(self.prioritize_tasks(tasks)):
            if self.total_time_used + task.duration > available_minutes:
                self.skipped_tasks.append(task)
                continue

            if not task.matches_preference(owner.preferences):
                self.skipped_tasks.append(task)
                continue

            self.selected_tasks.append(task)
            self.total_time_used += task.duration

        return list(self.selected_tasks)

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by preferred time, requirement, and priority."""
        return sorted(
            tasks,
            key=lambda task: (
                task.preferred_time,
                not task.required,
                -task.priority,
            ),
        )

    def explain_plan(
        self,
        selected_tasks: List[Task],
        skipped_tasks: List[Task],
    ) -> str:
        """Return a short summary of the selected and skipped tasks."""
        selected_titles = ", ".join(task.title for task in selected_tasks)
        skipped_titles = ", ".join(task.title for task in skipped_tasks)
        return (
            f"Selected: {selected_titles}. Skipped: {skipped_titles}. "
            f"Total time used: {self.total_time_used} minutes."
        )

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect tasks that have conflicting preferred times."""
        conflicts: List[str] = []
        seen_times: Dict[str, Task] = {}

        for task in tasks:
            if task.preferred_time in seen_times:
                conflicts.append(
                    f"{task.title} conflicts with {seen_times[task.preferred_time].title} "
                    f"at {task.preferred_time}"
                )
            else:
                seen_times[task.preferred_time] = task

        return conflicts
