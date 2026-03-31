# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
For my initial UML design, I created four main classes: Owner, Pet, Task, and Scheduler. I chose these classes because they represent the main parts of the PawPal+ system. The Owner class is responsible for storing information about the user, including their available time and any preferences that affect scheduling. The Pet class represents the pet and stores details such as name, species, and a list of care tasks. The Task class represents individual care activities like feeding, walking, or medication, and includes important attributes such as duration, priority, and whether the task is required or recurring. The Scheduler class is responsible for the main logic of the system, including organizing tasks, prioritizing them based on importance, and generating a daily plan. It also handles explaining why certain tasks were selected or skipped. I designed the system this way to keep responsibilities separated and make the logic easier to manage and expand.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Use Scheduler with an Owner object instead of separate tasks, available_minutes, and preferences.
This keeps scheduling logic tied to the owner and avoids disconnecting data.
Replace loose Dict[str, str] preferences with a clearer structure.
This makes matches_preference() easier to implement and less error-prone.
Add a helper to gather all pet tasks from an owner.
This ensures the scheduler sees every pet task and doesn’t miss anything.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
