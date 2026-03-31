from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


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
        pass

    def mark_incomplete(self) -> None:
        pass

    def update_priority(self, priority: int) -> None:
        pass

    def matches_preference(self, preferences: Dict[str, str]) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_title: str) -> None:
        pass

    def edit_task(self, task_title: str, updated_task: Task) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


class Owner:
    def __init__(
        self,
        name: str,
        available_minutes: int = 0,
        preferences: Optional[Dict[str, str]] = None,
    ):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_name: str) -> None:
        pass

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        pass

    def update_available_time(self, minutes: int) -> None:
        pass

    def set_preference(self, key: str, value: str) -> None:
        pass


class Scheduler:
    def __init__(self) -> None:
        self.selected_tasks: List[Task] = []
        self.skipped_tasks: List[Task] = []
        self.total_time_used: int = 0

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        pass

    def build_daily_plan(
        self,
        tasks: List[Task],
        available_minutes: int,
        preferences: Dict[str, str],
    ) -> List[Task]:
        pass

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        pass

    def explain_plan(
        self,
        selected_tasks: List[Task],
        skipped_tasks: List[Task],
    ) -> str:
        pass

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        pass
