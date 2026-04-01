# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

For my initial UML design, I created four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`.
- `Owner` stores the pet owner’s information, available time, preferences, and pets.
- `Pet` holds pet details plus a list of care tasks.
- `Task` models a single care activity with attributes like duration, priority, required status, recurrence, and completion.
- `Scheduler` is the planning engine, responsible for organizing tasks, prioritizing them, building a daily plan, and detecting conflicts.

This design kept responsibilities separated so the data model and scheduling logic were easy to extend.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, the design evolved during implementation.
- I changed `Scheduler` to work directly with an `Owner` object instead of passing tasks, available minutes, and preferences separately. This made the scheduling interface more coherent and reduced the chances of disconnected data.
- I added `Owner.get_all_tasks()` so the scheduler could aggregate tasks from every pet cleanly.
- I also extended `Task` to support `frequency` and `due_date`, and added `Task.create_next_occurrence()` so recurring tasks can generate their next instance automatically.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers:
- `preferred_time` for ordering tasks by when they should happen.
- task `priority` to decide which important tasks should be selected first.
- `required` status to keep essential pet care tasks prioritized.
- completion status so completed, non-recurring tasks are skipped.
- owner preferences and pet name filters to display relevant tasks.

I chose these constraints because they reflect realistic pet-care planning: owners need tasks sorted by time, important work should come first, and recurring maintenance should stay on the schedule.

**b. Tradeoffs**

- The scheduler only checks for exact preferred-time matches when detecting conflicts, rather than modeling task durations and overlapping time windows.
- This tradeoff is reasonable because it keeps conflict detection lightweight and easy to understand for a simple pet care planner, while still catching the most obvious scheduling problems.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI for design brainstorming, code generation, refactoring, and debugging.
- I asked Copilot to suggest class relationships and method signatures for the UML design.
- I used AI to implement scheduler methods like sorting, filtering, recurring task handling, and conflict detection.
- I also used AI to draft tests and improve README documentation.

The most helpful prompts were direct questions about method behavior, such as "How can I sort Task objects by HH:MM time?" and "What is a lightweight way to detect scheduling conflicts?"

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I rejected a suggestion that overcomplicated conflict detection by modeling task durations and overlap windows. Instead, I kept a simpler exact-time conflict strategy because it was easier to read, maintain, and fit the app’s current scope.

I verified AI suggestions by testing the behavior in `main.py` and with pytest. If a suggestion made the code harder to reason about, I simplified it while preserving the feature.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested:
- task completion behavior to ensure `mark_complete()` updates status correctly,
- task addition to ensure adding a task to a pet increases the pet’s task count,
- recurring task behavior to confirm completing a daily task creates a next occurrence,
- conflict detection to confirm the scheduler flags duplicate preferred times.

These tests were important because they verify the core scheduling behaviors and the features that make PawPal+ smart.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am reasonably confident in the scheduler for the current app scope, especially for sorting tasks, recurring daily tasks, and exact-time conflict detection.

Next edge cases to test would include:
- a pet with no tasks,
- recurring tasks that already have a due date in the past,
- owner preferences that filter out all tasks,
- tasks with invalid or missing preferred times.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with turning the scheduler into a usable logic layer that supports sorting, filtering, recurrence, and lightweight conflict warnings while staying easy to understand.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve conflict handling by modeling task durations and overlapping time windows more formally, and I would add a richer preference schema for the owner.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that as the lead architect, my role is to guide AI suggestions toward clarity and simplicity, choose the right abstraction for the problem, and verify behavior with tests rather than accepting generated code blindly.
