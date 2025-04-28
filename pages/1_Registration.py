import streamlit as st

st.title("📝 User Registration - CognitiveCare")

st.markdown("""
Please fill out the questionnaire below to **register your profile**. This helps us tailor your Alzheimer's prevention and progression management experience.
""")

# User input form
age = st.number_input("Enter your age", min_value=18, max_value=120, value=50)
sleep_hours = st.slider("How many hours of sleep do you get per night?", 0, 12, 7)
diet = st.selectbox("Select your diet type", ["MIND Diet", "Mediterranean Diet", "High-fat Diet", "Vegetarian", "Other"])
activity_level = st.selectbox("Select your physical activity level", ["None", "Light (1-2 times/week)", "Moderate (3-4 times/week)", "High (5+ times/week)"])
medical_conditions = st.multiselect(
    "Do you have any of the following medical conditions?",
    ["Hypertension", "Diabetes", "High cholesterol", "None"]
)
cognitive_engagement = st.selectbox(
    "How often do you engage in cognitive activities (puzzles, reading, learning)?",
    ["Rarely", "Sometimes", "Regularly"]
)


# Save the user's profile into session_state
if st.button("Register Profile"):
    st.session_state.user_profile = {
        "age": age,
        "sleep_hours": sleep_hours,
        "diet": diet,
        "activity_level": activity_level,
        "medical_conditions": medical_conditions,
        "cognitive_engagement": cognitive_engagement
    }
    st.success("Your profile has been registered successfully!")

