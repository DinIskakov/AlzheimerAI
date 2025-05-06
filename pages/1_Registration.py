import streamlit as st

st.set_page_config(page_title="ValeriaAI Registration", layout="centered")
st.title("📝 Register Your Profile")

st.markdown("""
Welcome to **CognitiveCare**, your AI companion for Alzheimer's support.
Please fill in the essential details below to personalize your experience.
""")

# --- Essential Fields ---
st.header("👤 Personal Information")

age = st.number_input("Age", min_value=18, max_value=120, value=60)
diagnosis_stage = st.selectbox("Diagnosis Stage", ["Early", "Middle", "Late"])

st.header("🛌 Lifestyle & Activity")
sleep_hours = st.slider("Average Sleep per Night (hours)", 0, 12, 7)
activity_level = st.selectbox("Physical Activity Level", ["None", "Light", "Moderate", "High"])
cognitive_engagement = st.selectbox("Cognitive Engagement Frequency", ["Rarely", "Sometimes", "Regularly"])

st.header("🏥 Medical Background")
medical_conditions = st.multiselect(
    "Do you have any of these conditions?",
    ["Hypertension", "Diabetes", "Depression", "None"]
)

# --- Submit Button ---
if st.button("Register Profile"):
    st.session_state.user_profile = {
        "age": age,
        "diagnosis_stage": diagnosis_stage,
        "sleep_hours": sleep_hours,
        "activity_level": activity_level,
        "cognitive_engagement": cognitive_engagement,
        "medical_conditions": medical_conditions
    }
    st.success("✅ Profile registered successfully!")
    #st.write("### Saved Profile:")
    #st.json(st.session_state.user_profile)
else:
    st.info("Fill out your details and click 'Register Profile' to continue.")
