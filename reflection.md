# PawPal+ Project Reflection

## 1. System Design

The user should be able to add a pet, add a task and modify it, and view an organized plan of the tasks for the day. 

**a. Initial design**

- Briefly describe your initial UML design.
    My design had four classes: Owner, Pet, Task, and Scheduler. The Owner and Pet classes hold the data, and the Scheduler contains the logic that turns a list of tasks into a daily plan. Claude also initially suggested that I add a ScheduledTask class for tasks that have a specific time.
- What classes did you include, and what responsibilities did you assign to each?
    Owner – stores basic user info and the available time for the day, and owns a list of pets.
    Pet – stores the pet's details and its list of tasks, with methods to add, edit, and remove them.
    Task – represents one care activity: its name, duration, priority, and category.
    Scheduler – takes the tasks and available time and produces the daily plan.
    ScheduledTask - stores a task in addition to a concrete start time.

**b. Design changes**

- Did your design change during implementation?
    I made a few changes based on AI feedback.
- If yes, describe at least one change and why you made it.
    I removed the ScheduledTask class and added a time attribute to the Task class. This way, if the time is set, then the task is properly scheduled. If not, then the task probably does not fit in the schedule. I believe that having an extra class would overcomplicate the code.
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
