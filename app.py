import streamlit as st

st.set_page_config(page_title="CognitiveCare Home", layout="centered")
st.title("🧠 Welcome to ValeriaAI!")

st.markdown("""
### Your Personal Cognitive Care Companion

Vale is designed to support individuals affected by Alzheimer's disease and their caregivers. Our AI-powered platform offers:

- 🤖 **Intelligent Assistant**: A compassionate AI companion that understands your needs and adapts to your cognitive stage
- 📅 **Calendar Management**: Chat integrated calendar management allowing you to schedule appointments, reminders, and activities
- 🎯 **Brain Training**: Engaging cognitive exercises including memory games, puzzles, and language learning
- 📋 **Personalized Care**: Tailored support based on your profile and specific needs

#### Getting Started
1. Create your profile in the **Profile** section
2. Connect with your AI companion in the **Chat** section
3. Explore brain-stimulating activities in the **Activities** section
4. View your calendar in the **Calendar** section

*Valeria is here to support you on your every step*
""")

if not st.session_state.get("user_profile"):
    st.info("👈 Please start by creating your profile in the Profile section.")
