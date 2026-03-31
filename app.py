import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=120)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.subheader("Owner")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value=owner.name)
with col2:
    available_minutes = st.number_input(
        "Available minutes",
        min_value=0,
        max_value=1440,
        value=owner.available_minutes,
    )

if st.button("Update owner"):
    owner.name = owner_name
    owner.available_minutes = available_minutes
    st.success("Owner updated.")

st.divider()

st.subheader("Add a Pet")
with st.form("pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="Mixed")
    age = st.number_input("Age", min_value=0, max_value=30, value=2)
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    new_pet = Pet(name=pet_name, species=species, breed=breed, age=age)
    owner.add_pet(new_pet)
    st.success(f"Added pet {pet_name}.")

if owner.pets:
    st.markdown("### Pets")
    for pet in owner.pets:
        st.write(f"- **{pet.name}** ({pet.species}, {pet.breed}, {pet.age} yrs)")
else:
    st.info("No pets yet. Add a pet above.")

st.divider()

if owner.pets:
    st.subheader("Add a Task")
    pet_names = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Select pet", pet_names)
    selected_pet = owner.get_pet(selected_pet_name)

    with st.form("task_form"):
        task_title = st.text_input("Task title", value="Morning walk")
        category = st.selectbox("Category", ["care", "exercise", "health", "grooming"])
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        preferred_time = st.text_input("Preferred time", value="08:00")
        required = st.checkbox("Required", value=True)
        notes = st.text_area("Notes", value="")
        add_task = st.form_submit_button("Add task")

    if add_task and selected_pet:
        priority_value = {"low": 1, "medium": 5, "high": 10}[priority]
        selected_pet.add_task(
            Task(
                title=task_title,
                category=category,
                duration=int(duration),
                priority=priority_value,
                preferred_time=preferred_time,
                required=required,
                notes=notes,
            )
        )
        st.success(f"Added task '{task_title}' to {selected_pet.name}.")

    st.divider()

    st.subheader("Current Tasks by Pet")
    for pet in owner.pets:
        if pet.tasks:
            st.markdown(f"**{pet.name}**")
            for task in pet.tasks:
                st.markdown(
                    f"- {task.title} ({task.category}) — {task.duration} min, priority {task.priority}, "
                    f"preferred {task.preferred_time}, {'required' if task.required else 'optional'}"
                )
        else:
            st.markdown(f"**{pet.name}** has no tasks yet.")

    st.divider()

    st.subheader("Build Schedule")
    if st.button("Generate schedule"):
        plan = scheduler.build_daily_plan(owner)
        if plan:
            st.markdown("### Today's Schedule")
            for index, task in enumerate(plan, start=1):
                st.write(
                    f"{index}. {task.title} ({task.category}) — {task.duration} min, "
                    f"{task.preferred_time}, {task.priority} priority, "
                    f"Pet: {next(pet.name for pet in owner.pets if task in pet.tasks)}"
                )
        else:
            st.warning("No tasks could fit in the selected time or preferences.")

        if scheduler.conflicts:
            st.warning("Scheduling conflicts detected:")
            for conflict in scheduler.conflicts:
                st.write(f"- {conflict}")

        st.info(scheduler.explain_plan(scheduler.selected_tasks, scheduler.skipped_tasks))
else:
    st.info("Add a pet first to start assigning tasks.")
