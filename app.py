import streamlit as st
import pandas as pd
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart English System", layout="wide")

# ---------------- DATA ----------------
lessons = {
    "A1": ["Greetings", "Numbers", "Colors"],
    "A2": ["Past Tense", "Daily Routine", "Food"],
    "B1": ["Opinions", "Travel", "Work"]
}

questions = {
    "Greetings": [
        {"q": "How do you say 'Hola'?", "a": "Hello"},
        {"q": "Good morning in Spanish?", "a": "Buenos días"}
    ],
    "Numbers": [
        {"q": "Number after 5?", "a": "6"},
        {"q": "Number before 10?", "a": "9"}
    ]
}

# ---------------- SIDEBAR ----------------
menu = st.sidebar.selectbox("Menu", [
    "Dashboard",
    "Courses",
    "Smart Mode",
    "Challenges",
    "Teacher Panel"
])

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.title("📊 Dashboard")

    progress = random.randint(10, 90)

    st.metric("Your Progress", f"{progress}%")
    st.progress(progress)

    st.info("🔥 Recommendation: Practice Greetings today")

# ---------------- COURSES ----------------
elif menu == "Courses":
    st.title("📚 Courses")

    level = st.selectbox("Select Level", list(lessons.keys()))

    st.subheader(f"Level {level}")

    for lesson in lessons[level]:
        if st.button(f"Start {lesson}"):
            st.session_state["lesson"] = lesson

    if "lesson" in st.session_state:
        lesson = st.session_state["lesson"]
        st.success(f"Lesson: {lesson}")

        if lesson in questions:
            q = random.choice(questions[lesson])
            answer = st.text_input(q["q"])

            if st.button("Submit"):
                if answer.lower() == q["a"].lower():
                    st.success("Correct ✅")
                else:
                    st.error(f"Incorrect ❌ Answer: {q['a']}")

# ---------------- SMART MODE ----------------
elif menu == "Smart Mode":
    st.title("🧠 Smart Mode")

    errors = ["Greetings", "Numbers", "Past Tense"]
    recommendation = random.choice(errors)

    st.warning(f"⚡ You need to improve: {recommendation}")

# ---------------- CHALLENGES ----------------
elif menu == "Challenges":
    st.title("🎮 Daily Challenge")

    challenge = "Translate: 'Buenos días'"
    answer = st.text_input(challenge)

    if st.button("Check"):
        if answer.lower() == "good morning":
            st.success("🔥 +10 points")
        else:
            st.error("Try again")

# ---------------- TEACHER PANEL ----------------
elif menu == "Teacher Panel":
    st.title("📊 Teacher Panel")

    data = pd.DataFrame({
        "Student": ["Juan", "Maria", "Luis"],
        "Score": [80, 90, 70]
    })

    st.dataframe(data)

    st.download_button(
        "Download Report",
        data.to_csv(index=False),
        file_name="report.csv"
    )
