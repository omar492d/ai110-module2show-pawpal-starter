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
    The scheduler first considers the priority of the tasks; more important tasks must be scheduled first. After that, tasks with a longer duration get scheduled. 
- How did you decide which constraints mattered most?
    Higher priority tasks are likely more important to the user, so it is necessary to schedule them first, even if that means no other tasks can fit the plan. Duration is also an important constraint because it allows the user to make the most of their remaining time.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    One tradeoff my scheduler makes is that it packs tasks greedily by priority against a single pool of available minutes, rather than placing them on a real clock-based timeline. It sorts tasks so the highest-priority ones are chosen first and simply drops the rest once the time budget runs out. This is fast (one pass through the tasks) and easy to reason about, and it guarantees that the most important care tasks are never skipped in favor of trivial ones.
- Why is that tradeoff reasonable for this scenario?
    The downside is that it doesn't reason about when tasks actually happen, so two tasks can be assigned the same preferred time without the scheduler resolving it — which is why conflict detection is handled separately as an advisory warning. For this scenario that tradeoff is reasonable: a pet owner's day has only a handful of tasks, so a simple priority-first plan is predictable and good enough, and surfacing conflicts as a warning lets the owner make the final call instead of the program guessing.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    I used AI for many parts of developing this project. On several times, I relied on it to modify the core logic to make the app more functional and add new features. AI was also very useful in creating tests and identifying important edge cases.
- What kinds of prompts or questions were most helpful?
    I had a lot of success with asking AI to explain how different parts of the project work together. With every new feature added, it was getting harder to keep up with the complexity of the code. But AI provided me with an understanding of the entire system and also explained why some methods were designed that way.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    When brainstorming the classes, Claude suggested that I add a "pet" reference to the Task class. This would have been for determining which pet owns the task, and it may have also been used for the filter feature. However, I rejected this as it would have added more complexity to the class.
- How did you evaluate or verify what the AI suggested?
    I first realized that the pet class already references all its tasks. Adding a new pet reference to Task might have created new issues. For example, what would happen if I add a task to Mochi, but accidentally set the pet reference to Max? I thought that adding this attribute was unnecessary unless there was a feature that definitely required it. 
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    I tested all aspects of the program, including adding a task, sorting according to time, and conflict detection. 
- Why were these tests important?
    These tests helped determine if there is any flawed logic and ensured that the functions behaved as expected. The entire program depends on these features and it is absolutely crucial that they function properly, especially when faced with weird inputs.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    I am highly confident in the scheduler. The tests showcased that it can successfully generate a schedule that fits the time constraints and display the tasks in a clear and organized manner. 
- What edge cases would you test next if you had more time?
    I would test what would happen if there are several combinations of tasks that fit the schedule. For example, imagine there are 60 minutes available and there are tasks with the following durations: 50 minutes, 30 minutes, 15 minutes, and 30 minutes. What tasks should the scheduler pick?
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I am satisfied with how the logic has been implemented. It takes advantage of many powerful python features, such as enums and list comprehensions. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I would improve the way the UI interacts with the logic to make it more efficient and understandable. I would allow the user to view all their saved pets at the same time and allow them to change the details of their tasks.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    When designing large systems, it is really easy to lose track of the changes and blindly follow the AI's suggestions. There are many parts interacting together and it may seem easier to let the AI take care of them. However, it is important that the programmer, not the AI, stays in control of the project and its many decisions.
