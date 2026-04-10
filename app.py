import streamlit as st
import pandas as pd
import random
import json
from collections import Counter

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Smart English System", layout="wide")

# ---------------- LOGIN ----------------
users = {
    "teacher": "1234",
    "student": "abcd"
}

if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    st.title("🔐 Login")

    user = st.text_input("User")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user in users and users[user] == pwd:
            st.session_state.logged = True
            st.success("Welcome 🚀")
        else:
            st.error("Wrong credentials")

    st.stop()

# ---------------- SESSION STATE ----------------
if "xp" not in st.session_state:
    st.session_state.xp = 0

if "level" not in st.session_state:
    st.session_state.level = 1

if "streak" not in st.session_state:
    st.session_state.streak = 1

if "errors" not in st.session_state:
    st.session_state.errors = []

# ---------------- SAVE / LOAD ----------------
def save_data():
    data = {
        "xp": st.session_state.xp,
        "level": st.session_state.level,
        "errors": st.session_state.errors
    }
    with open("user_data.json", "w") as f:
        json.dump(data, f)

def load_data():
    try:
        with open("user_data.json") as f:
            data = json.load(f)
            st.session_state.xp = data["xp"]
            st.session_state.level = data["level"]
            st.session_state.errors = data["errors"]
    except:
        pass

load_data()

# ---------------- XP SYSTEM ----------------
def add_xp(points):
    st.session_state.xp += points

    if st.session_state.xp >= 50:
        st.session_state.level += 1
        st.session_state.xp = 0
        st.success("🚀 LEVEL UP!")

# ---------------- DATA ----------------
lessons = {
    "A1": ["Greetings", "Numbers"],
    "A2": ["Past Tense"],
    "B1": ["Opinions"]
}

questions = {
    "Greetings": [
        {"q": "How do you say 'Hola'?", "a": "hello"},
        {"q": "Good morning in Spanish?", "a": "buenos días"}
    ],
    "Numbers": [
        {"q": "Number after 5?", "a": "6"},
        {"q": "Number before 10?", "a": "9"}
    ],
    "Past Tense": [
        {"q": "Past of 'go'?", "a": "went"}
    ]
}

# ---------------- MENU ----------------
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

    st.metric("Level", st.session_state.level)
    st.metric("XP", st.session_state.xp)
    st.metric("Streak 🔥", st.session_state.streak)

    progress = min(st.session_state.xp, 100)
    st.progress(progress)

    st.info("🔥 Recommendation: Practice your weakest topic")

# ---------------- COURSES ----------------
elif menu == "Courses":
    st.title("📚 Courses")

    level = st.selectbox("Select Level", list(lessons.keys()))

    st.subheader(f"Level {level}")

    for lesson in lessons[level]:
        if st.button(f"Start {lesson}"):
            st.session_state.lesson = lesson

    if "lesson" in st.session_state:
        lesson = st.session_state.lesson
        st.success(f"Lesson: {lesson}")

        if lesson in questions:
            q = random.choice(questions[lesson])
            answer = st.text_input(q["q"])

            if st.button("Submit"):
                if answer.lower() == q["a"]:
                    add_xp(10)
                    st.success("Correct ✅ +10 XP")
                    save_data()
                else:
                    st.error(f"Incorrect ❌ Answer: {q['a']}")
                    st.session_state.errors.append(lesson)
                    save_data()

# ---------------- SMART MODE ----------------
elif menu == "Smart Mode":
    st.title("🧠 Smart Mode")

    if st.session_state.errors:
        most_common = Counter(st.session_state.errors).most_common(1)[0][0]
        st.warning(f"⚡ Focus here: {most_common}")
    else:
        st.success("No weaknesses detected 🚀")

# ---------------- CHALLENGES ----------------
elif menu == "Challenges":
    st.title("🎮 Daily Challenge")

    challenge = "Translate: 'Buenos días'"
    answer = st.text_input(challenge)

    if st.button("Check"):
        if answer.lower() == "good morning":
            add_xp(10)
            st.success("🔥 +10 XP")
            save_data()
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
