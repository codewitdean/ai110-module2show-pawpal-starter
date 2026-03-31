from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
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
    frequency: Optional[str] = None
    completed: bool = False
    notes: str = ""
    due_date: Optional[date] = None

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed and return the next recurring instance if needed."""
        self.completed = True
        return self.create_next_occurrence()

    def create_next_occurrence(self) -> Optional["Task"]:
        """Return a new Task for the next daily or weekly occurrence."""
        if self.frequency not in {"daily", "weekly"}:
            return None

        next_due_date = self.due_date or date.today()
        if self.frequency == "daily":
            next_due_date += timedelta(days=1)
        else:
            next_due_date += timedelta(weeks=1)

        return Task(
            title=self.title,
            category=self.category,
            duration=self.duration,
            priority=self.priority,
            preferred_time=self.preferred_time,
            required=self.required,
            recurring=self.recurring,
            frequency=self.frequency,
            completed=False,
            notes=self.notes,
            due_date=next_due_date,
        )

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
        self.conflicts: List[str] = []
        self.total_time_used: int = 0

    def parse_preferred_time(self, preferred_time: str) -> int:
        """Convert a preferred time like '08:00' into minutes since midnight."""
        try:
            parsed = datetime.strptime(preferred_time, "%H:%M")
            return parsed.hour * 60 + parsed.minute
        except ValueError:
            return 24 * 60

    def filter_tasks(self, tasks: List[Task], preferences: Optional[Preferences] = None) -> List[Task]:
        """Filter tasks based on owner preferences like category, status, and requirement."""
        preferences = preferences or {}
        filtered: List[Task] = []

        for task in tasks:
            if not task.matches_preference(preferences):
                continue

            if "status" in preferences:
                status = "completed" if task.completed else "pending"
                if preferences["status"] != status:
                    continue

            if "required" in preferences:
                required_value = preferences["required"].lower()
                if required_value in {"true", "yes", "1"} and not task.required:
                    continue
                if required_value in {"false", "no", "0"} and task.required:
                    continue

            filtered.append(task)

        return filtered

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by requirement, priority, and shorter duration."""
        return sorted(
            tasks,
            key=lambda task: (
                not task.required,
                -task.priority,
                task.duration,
            ),
        )

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by preferred time, required flag, and priority."""
        return sorted(
            tasks,
            key=lambda task: (
                self.parse_preferred_time(task.preferred_time),
                not task.required,
                -task.priority,
            ),
        )

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their preferred time using a lambda function on HH:MM strings."""
        return self.sort_tasks(tasks)

    def filter_tasks_by_status(self, tasks: List[Task], completed: bool) -> List[Task]:
        """Return tasks that match the completed status."""
        return [task for task in tasks if task.completed == completed]

    def filter_tasks_by_pet_name(self, owner: Owner, pet_name: str) -> List[Task]:
        """Return all tasks for the pet with the given name."""
        pet = owner.get_pet(pet_name)
        return pet.get_tasks() if pet else []

    def should_schedule(self, task: Task) -> bool:
        """Decide whether a task should be included in today's schedule."""
        if task.completed:
            return False

        if task.due_date and task.due_date > date.today():
            return False

        return True

    def resolve_conflicts(self, tasks: List[Task]) -> List[Task]:
        """Keep one task per preferred time and skip lower-priority conflicts."""
        self.conflicts = self.detect_conflicts(tasks)

        tasks_by_time: Dict[int, List[Task]] = defaultdict(list)
        for task in tasks:
            tasks_by_time[self.parse_preferred_time(task.preferred_time)].append(task)

        resolved: List[Task] = []

        for time_key, group in tasks_by_time.items():
            if len(group) == 1:
                resolved.append(group[0])
                continue

            group.sort(key=lambda task: (not task.required, -task.priority, task.duration))
            winner = group[0]
            resolved.append(winner)

            for loser in group[1:]:
                self.conflicts.append(
                    f"{loser.title} conflicts with {winner.title} at {winner.preferred_time}"
                )

        return resolved

    def complete_task(self, owner: Owner, pet_name: str, task_title: str) -> Optional[Task]:
        """Mark the matching task complete and add its next occurrence if it recurs."""
        pet = owner.get_pet(pet_name)
        if pet is None:
            return None

        for task in pet.tasks:
            if task.title == task_title and not task.completed:
                next_task = task.mark_complete()
                if next_task is not None:
                    pet.add_task(next_task)
                return next_task

        return None

    def build_daily_plan(self, owner: Owner) -> List[Task]:
        """Build a daily task schedule for the given owner."""
        self.owner = owner
        self.selected_tasks = []
        self.skipped_tasks = []
        self.total_time_used = 0
        self.conflicts = []

        tasks = owner.get_all_tasks()
        tasks = [task for task in tasks if self.should_schedule(task)]
        tasks = self.filter_tasks(tasks, owner.preferences)
        tasks = self.resolve_conflicts(tasks)

        for task in self.sort_tasks(tasks):
            if self.total_time_used + task.duration > owner.available_minutes:
                self.skipped_tasks.append(task)
                continue

            self.selected_tasks.append(task)
            self.total_time_used += task.duration

        return list(self.selected_tasks)

    def explain_plan(
        self,
        selected_tasks: List[Task],
        skipped_tasks: List[Task],
    ) -> str:
        """Return a short summary of the selected and skipped tasks."""
        selected_titles = ", ".join(task.title for task in selected_tasks)
        skipped_titles = ", ".join(task.title for task in skipped_tasks)
        conflict_text = " ".join(self.conflicts)

        summary = (
            f"Selected: {selected_titles}. Skipped: {skipped_titles}. "
            f"Total time used: {self.total_time_used} minutes."
        )
        if self.conflicts:
            summary += f" Conflicts: {conflict_text}."
        return summary

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect tasks that have conflicting preferred times and return warnings."""
        conflicts: List[str] = []
        tasks_by_time: Dict[str, List[Task]] = defaultdict(list)

        for task in tasks:
            tasks_by_time[task.preferred_time].append(task)

        for preferred_time, group in tasks_by_time.items():
            if len(group) > 1:
                task_titles = ", ".join(task.title for task in group)
                conflicts.append(
                    f"Conflict at {preferred_time}: {task_titles} are scheduled at the same time."
                )

        return conflicts
