import streamlit as st
import random
from datetime import datetime

# Initialize session state for activity tracking
if 'activity_log' not in st.session_state:
    st.session_state.activity_log = []

# Page Title
st.title("🧠 Cognitive Activities")

st.markdown("""
Welcome to the Cognitive Activities section! Engage in exercises designed to stimulate memory, attention, and language skills.
""")

# Activity Selection
activity = st.selectbox(
    "Choose an activity:",
    ["Memory Match", "Language Learning", "Number Puzzle"]
)

def memory_match():
    st.subheader("🧩 Memory Match")
    st.markdown("Find all the matching pairs. Click two cards to reveal them, then click Continue to check for a match.")

    base_values = ['🍎', '🐶', '🎵', '🚗', '🌼', '📚']
    total_cards = len(base_values) * 2
    cols_per_row = 4

    # Initialize
    if "mm_board" not in st.session_state:
        cards = base_values * 2
        random.shuffle(cards)
        st.session_state.mm_board = cards
        st.session_state.mm_flipped = []
        st.session_state.mm_matched = []
        st.session_state.mm_turns = 0
        st.session_state.mm_waiting_to_check = False

    def reset_game():
        cards = base_values * 2
        random.shuffle(cards)
        st.session_state.mm_board = cards
        st.session_state.mm_flipped = []
        st.session_state.mm_matched = []
        st.session_state.mm_turns = 0
        st.session_state.mm_waiting_to_check = False
        st.experimental_rerun()

    # Create consistent 4x3 grid
    for row in range(3):  # 3 rows
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            i = row * cols_per_row + col_idx
            card_val = st.session_state.mm_board[i]
            flipped = i in st.session_state.mm_flipped or i in st.session_state.mm_matched

            with cols[col_idx]:
                if flipped:
                    st.button(card_val, key=f"card_{i}", disabled=True)
                else:
                    if not st.session_state.mm_waiting_to_check:
                        if st.button("❓", key=f"card_{i}"):
                            if i not in st.session_state.mm_flipped and len(st.session_state.mm_flipped) < 2:
                                st.session_state.mm_flipped.append(i)
                                if len(st.session_state.mm_flipped) == 2:
                                    st.session_state.mm_waiting_to_check = True
                                    st.experimental_rerun()

    # Matching logic
    if st.session_state.mm_waiting_to_check and len(st.session_state.mm_flipped) == 2:
        idx1, idx2 = st.session_state.mm_flipped
        val1 = st.session_state.mm_board[idx1]
        val2 = st.session_state.mm_board[idx2]
        st.info(f"You flipped: {val1} and {val2}")

        if st.button("✅ Continue"):
            st.session_state.mm_turns += 1
            if val1 == val2:
                st.session_state.mm_matched.extend([idx1, idx2])
            st.session_state.mm_flipped = []
            st.session_state.mm_waiting_to_check = False
            st.experimental_rerun()

    st.markdown("---")
    st.write(f"**Turns Taken:** {st.session_state.mm_turns}")

    if len(st.session_state.mm_matched) == total_cards:
        st.success("🎉 Great job! You've matched all the pairs!")
        st.button("🔁 Play Again", on_click=reset_game)

    st.button("🔄 Reset Game", on_click=reset_game)
    
# Function: Language Learning
def language_learning():
    st.subheader("🌍 Language Learning")
    st.markdown("Practice basic vocabulary in different languages.")

    # Word banks
    languages = {
        "Spanish": {"Hello": "Hola", "Thank you": "Gracias", "Goodbye": "Adiós"},
        "French": {"Hello": "Bonjour", "Thank you": "Merci", "Goodbye": "Au revoir"},
    }

    # Select language
    selected_lang = st.selectbox("Choose a language:", list(languages.keys()), key="lang_choice")

    # Initialize state (only once or when switching languages)
    if "lang_word" not in st.session_state or st.session_state.get("lang_last") != selected_lang:
        st.session_state.lang_word = random.choice(list(languages[selected_lang].keys()))
        st.session_state.lang_result_shown = False
        st.session_state.lang_last = selected_lang

    current_word = st.session_state.lang_word
    correct_translation = languages[selected_lang][current_word]

    st.write(f"**Translate:** {current_word}")
    user_input = st.text_input("Your translation:", key="lang_input")

    # Check answer
    if st.button("Check Translation") and not st.session_state.lang_result_shown:
        correct = user_input.strip().lower() == correct_translation.lower()
        st.session_state.lang_result_shown = "correct" if correct else "incorrect"

        # Log the result
        if "activity_log" not in st.session_state:
            st.session_state.activity_log = []

        st.session_state.activity_log.append({
            "activity": f"Language ({selected_lang})",
            "result": "Correct" if correct else "Incorrect",
            "timestamp": datetime.now()
        })

        st.experimental_rerun()

    # Show result
    if st.session_state.lang_result_shown:
        if st.session_state.lang_result_shown == "correct":
            st.success("✅ Correct! Well done.")
        else:
            st.error(f"❌ Incorrect. The correct translation was '{correct_translation}'.")

        if st.button("Next Word"):
            st.session_state.lang_word = random.choice(list(languages[selected_lang].keys()))
            st.session_state.lang_result_shown = False
            del st.session_state["lang_input"]
            st.experimental_rerun()


def number_puzzle():
    st.subheader("🔢 Number Puzzle")
    st.markdown("Solve the simple arithmetic problem.")

    if "np_num1" not in st.session_state:
        st.session_state.np_num1 = random.randint(1, 10)
        st.session_state.np_num2 = random.randint(1, 10)
        st.session_state.np_op = random.choice(["+", "-", "*"])
    if "np_result_shown" not in st.session_state:
        st.session_state.np_result_shown = False
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = []

    num1 = st.session_state.np_num1
    num2 = st.session_state.np_num2
    op = st.session_state.np_op

    st.write(f"**Problem:** {num1} {op} {num2} = ?")
    user_answer = st.number_input("Your answer:", step=1, key="np_input")

    #Check answer 
    if st.button("Check Answer") and not st.session_state.np_result_shown:
        if op == "+":
            correct = num1 + num2
        elif op == "-":
            correct = num1 - num2
        else:
            correct = num1 * num2

        if user_answer == correct:
            st.session_state.np_feedback = "✅ Correct! Great job."
            result = "Correct"
        else:
            st.session_state.np_feedback = f"❌ Incorrect. The correct answer was {correct}."
            result = "Incorrect"

        st.session_state.np_result_shown = True

        # Log
        st.session_state.activity_log.append({
            "activity": "Number Puzzle",
            "result": result,
            "timestamp": datetime.now()
        })

        st.experimental_rerun()

    # feedback 
    if st.session_state.np_result_shown:
        if "Correct" in st.session_state.np_feedback:
            st.success(st.session_state.np_feedback)
        else:
            st.error(st.session_state.np_feedback)

        # Wait for user to continue
        if st.button("Next Puzzle"):
            # Reset everything
            st.session_state.np_num1 = random.randint(1, 10)
            st.session_state.np_num2 = random.randint(1, 10)
            st.session_state.np_op = random.choice(["+", "-", "*"])
            st.session_state.np_result_shown = False
            st.session_state.np_feedback = ""
            del st.session_state["np_input"]
            st.experimental_rerun()
        
        

        

# Activity Execution
if activity == "Memory Match":
    memory_match()
elif activity == "Language Learning":
    language_learning()
elif activity == "Number Puzzle":
    number_puzzle()

# Display Activity Log
st.markdown("---")
st.subheader("📈 Activity Log")
if st.session_state.activity_log:
    for log in st.session_state.activity_log:
        st.write(f"{log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - {log['activity']}")
else:
    st.write("No activities completed yet.")
