import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

PRIORITIES = ["low", "medium", "high"]
RECURRENCE = ["one-off", "daily", "weekly"]


# ----------------------------------------------------------------------------
# State
# ----------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=120)

owner: Owner = st.session_state.owner


def active_pet() -> Pet | None:
    """The pet currently being worked on (the most recently added), if any."""
    return st.session_state.get("pet")


# ----------------------------------------------------------------------------
# Sidebar: owner + pet
# ----------------------------------------------------------------------------
with st.sidebar:
    st.header("🐾 PawPal+")
    st.caption("A pet-care planning assistant.")

    st.subheader("Owner")
    owner.name = st.text_input("Owner name", value=owner.name)
    owner.available_minutes = int(
        st.number_input(
            "Available minutes today",
            min_value=0,
            max_value=1440,
            value=owner.available_minutes,
            step=15,
        )
    )

    st.divider()
    st.subheader("Pet")

    with st.form("add_pet_form", clear_on_submit=True):
        st.markdown("**Add a pet**")
        new_name = st.text_input("Name", value="")
        c1, c2 = st.columns(2)
        with c1:
            new_species = st.selectbox("Species", ["dog", "cat", "other"])
            new_age = st.number_input("Age", min_value=0, max_value=50, value=2)
        with c2:
            new_gender = st.selectbox("Gender", ["", "female", "male"])
            new_breed = st.text_input("Breed", value="")
        if st.form_submit_button("Add pet", use_container_width=True):
            name = new_name.strip()
            if not name:
                st.warning("Give the pet a name.")
            elif any(p.name == name for p in owner.pets):
                st.warning(f"A pet named {name} already exists.")
            else:
                pet = Pet(
                    name=name,
                    age=int(new_age),
                    species=new_species,
                    breed=new_breed.strip(),
                    gender=new_gender,
                )
                owner.add_pet(pet)
                st.session_state.pet = pet
                st.rerun()


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
st.title("🐾 PawPal+")
st.caption("Plan and order your pet's care tasks around the time you have.")

pet = active_pet()

if pet is None:
    st.info("👈 Add a pet in the sidebar to get started.")
    st.stop()

# --- Pet header --------------------------------------------------------------
details = " · ".join(
    part
    for part in [
        pet.species,
        pet.breed,
        pet.gender,
        f"{pet.age} yr" if pet.age else "",
    ]
    if part
)
st.subheader(f"🐶 {pet.name}")
if details:
    st.caption(details)

tasks_tab, schedule_tab = st.tabs(["📋 Tasks", "🗓️ Schedule"])

# ----------------------------------------------------------------------------
# Tasks tab
# ----------------------------------------------------------------------------
with tasks_tab:
    with st.form("add_task_form", clear_on_submit=True):
        st.markdown(f"**Add a task for {pet.name}**")
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            t_title = st.text_input("Title", value="Morning walk")
        with c2:
            t_duration = st.number_input("Minutes", min_value=1, max_value=240, value=20)
        with c3:
            t_priority = st.selectbox("Priority", PRIORITIES, index=2)

        c4, c5 = st.columns(2)
        with c4:
            t_time = st.text_input("Preferred time (HH:MM)", value="07:30")
        with c5:
            t_recurrence = st.selectbox("Repeats", RECURRENCE)

        if st.form_submit_button("Add task", use_container_width=True):
            if not t_title.strip():
                st.warning("Give the task a title.")
            else:
                pet.add_task(
                    Task(
                        name=t_title.strip(),
                        duration_minutes=int(t_duration),
                        priority=Priority[t_priority.upper()],
                        preferred_time=t_time.strip() or None,
                        recurrence=None if t_recurrence == "one-off" else t_recurrence,
                    )
                )
                st.rerun()

    st.divider()

    # --- Task list with filter, complete, remove -----------------------------
    header_col, filter_col = st.columns([2, 1])
    with header_col:
        st.markdown(f"### Tasks for {pet.name}")
    with filter_col:
        show = st.radio(
            "Show", ["All", "Pending", "Completed"], horizontal=True, label_visibility="collapsed"
        )

    completed_filter = {"All": None, "Pending": False, "Completed": True}[show]
    visible = owner.filter_tasks(pet_name=pet.name, completed=completed_filter)

    if not visible:
        st.info("No tasks to show. Add one above.")
    else:
        scheduler = Scheduler()
        for i, task in enumerate(visible):
            done_col, info_col, del_col = st.columns([0.5, 6, 0.8])
            with done_col:
                checked = st.checkbox(
                    "done",
                    value=task.completed,
                    key=f"done_{pet.name}_{i}_{task.name}",
                    label_visibility="collapsed",
                )
                if checked and not task.completed:
                    follow_up = scheduler.complete_task(pet, task)
                    if follow_up is not None:
                        st.toast(f"Next '{follow_up.name}' scheduled for {follow_up.due_date}.")
                    st.rerun()
            with info_col:
                title = f"~~{task.name}~~" if task.completed else f"**{task.name}**"
                badges = f"`{task.priority.name}` · {task.duration_minutes} min"
                if task.preferred_time:
                    badges += f" · ⏰ {task.preferred_time}"
                if task.recurrence:
                    badges += f" · 🔁 {task.recurrence}"
                st.markdown(f"{title}  \n{badges}")
            with del_col:
                if st.button("🗑️", key=f"del_{pet.name}_{i}_{task.name}", help="Remove task"):
                    pet.remove_task(task)
                    st.rerun()

# ----------------------------------------------------------------------------
# Schedule tab
# ----------------------------------------------------------------------------
with schedule_tab:
    st.caption(
        f"Fits each pet's tasks into {owner.available_minutes} available minutes — "
        "priority first, then ordered by time."
    )
    if st.button("Generate schedule", type="primary"):
        if not any(p.tasks for p in owner.pets):
            st.warning("Add some tasks before generating a schedule.")
        else:
            scheduler = Scheduler()
            plans = {p.name: scheduler.generate_plan(p, owner.available_minutes) for p in owner.pets}

            planned = [(p.name, t) for p in owner.pets for t in plans[p.name][0]]
            all_skipped = [(p.name, t) for p in owner.pets for t in plans[p.name][1]]

            ordered = scheduler.sort_by_time([t for _, t in planned])
            pet_of = {id(t): pet_name for pet_name, t in planned}

            if ordered:
                st.success(f"Scheduled {len(ordered)} task(s) for {owner.name}.")
                st.markdown("#### 🗓️ Today's Schedule")
                st.table(
                    [
                        {
                            "time": t.scheduled_time or "—",
                            "pet": pet_of[id(t)],
                            "task": t.name,
                            "priority": t.priority.name,
                            "minutes": t.duration_minutes,
                        }
                        for t in ordered
                    ]
                )
            else:
                st.info("No tasks fit the available time.")

            conflicts = scheduler.detect_conflicts(owner)
            if conflicts:
                for warning in conflicts:
                    st.warning(f"⚠️ {warning}")
            else:
                st.success("No time conflicts — every task has its own slot.")

            if all_skipped:
                st.markdown("#### ⏭️ Skipped (didn't fit the time budget)")
                st.table(
                    [
                        {
                            "pet": pet_name,
                            "task": t.name,
                            "priority": t.priority.name,
                            "minutes": t.duration_minutes,
                        }
                        for pet_name, t in all_skipped
                    ]
                )

            with st.expander("Why this plan?"):
                for p in owner.pets:
                    st.markdown(f"**{p.name}**")
                    st.code(scheduler.explain(plans[p.name]), language="text")
