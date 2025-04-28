import streamlit as st
from agents.companion import CognitiveCareAgent


st.title("💬 CognitiveCare AI Chat")

# Check if user has registered
if "user_profile" not in st.session_state:
    st.warning("⚠️ Please complete your registration first on the 'User Registration' page.")
    st.stop()  # Prevents further execution (stops the page here)

if "agent_instance" not in st.session_state:
    st.session_state.agent_instance = CognitiveCareAgent()


st.markdown("""
Chat with the **AI-powered assistant** to get personalized recommendations or ask questions about Alzheimer's prevention and management.
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you with Alzheimer's prevention today?"}]

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your message here..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Placeholder AI response (replace with real AI logic)
    #response = f"[AI-generated response to: '{prompt}']"
    ai_response = st.session_state.agent_instance.generate_response(prompt, st.session_state["user_profile"])

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    print(st.session_state.messages)
