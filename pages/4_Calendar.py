import streamlit.components.v1 as components
import streamlit as st

#st.set_page_config(page_title="Calendar", layout="wide")

st.title("💬 Calendar")

#<iframe src="https://calendar.google.com/calendar/embed?src=dinizkakov%40gmail.com&ctz=Europe%2FLondon" style="border: 0" width="800" height="600" frameborder="0" scrolling="no"></iframe>

st.markdown("""
    <style>
        section.main > div {
            max-width: 95%;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)
components.iframe(
            f"https://calendar.google.com/calendar/embed?src=dinizkakov%40gmail.com&ctz=Europe%2FLondon",
             width=1200, height=800, scrolling=False)


