import streamlit as st
import random
import time
from datetime import timedelta

# ---------------------
# Session State Setup
# ---------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "last_rerun" not in st.session_state:
    st.session_state.last_rerun = time.time()
if "show_matrix" not in st.session_state:
    st.session_state.show_matrix = False

# ---------------------
# Page Title
# ---------------------
st.set_page_config(page_title="Matrix Math Practice", layout="centered")
st.title("🧠 Matrix Math Practice App")

# ---------------------
# User Inputs
# ---------------------
n = st.slider("Select Matrix Size (n x n)", 2, 10, 5)
digits_col = st.number_input("Digits for Column Numbers", min_value=1, max_value=5, value=2)
digits_row = st.number_input("Digits for Row Numbers", min_value=1, max_value=5, value=2)
operation = st.selectbox("Choose Operation", ["Addition", "Subtraction", "Multiplication"])

# ---------------------
# Generate Random Numbers
# ---------------------
def generate_numbers(n, digits):
    min_val = 10 ** (digits - 1)
    max_val = (10 ** digits) - 1
    return [random.randint(min_val, max_val) for _ in range(n)]

# ---------------------
# Timer Placeholder
# ---------------------
timer_placeholder = st.empty()

# ---------------------
# Generate Matrix
# ---------------------
if st.button("🌀 Generate Matrix"):
    st.session_state.col_nums = generate_numbers(n, digits_col)
    st.session_state.row_nums = generate_numbers(n, digits_row)
    st.session_state.start_time = time.time()
    st.session_state.last_rerun = time.time()
    st.session_state.show_matrix = True

# ---------------------
# Display Matrix + Timer + Form
# ---------------------
if st.session_state.get("show_matrix", False):
    col_nums = st.session_state.col_nums
    row_nums = st.session_state.row_nums

    # ✅ Live Timer Display (Top-Right)
    if st.session_state.start_time:
        elapsed = int(time.time() - st.session_state.start_time)
        timer_placeholder.markdown(
            f"""
            <div style='position: fixed; top: 15px; right: 30px; background-color: #007ACC;
                        color: white; padding: 10px 20px; font-size: 18px; border-radius: 10px;
                        box-shadow: 0 0 10px rgba(0,0,0,0.15); z-index: 9999;'>
                ⏱️ <strong>{str(timedelta(seconds=elapsed))}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Re-run every 1 sec (non-blocking)
        if time.time() - st.session_state.last_rerun >= 1:
            st.session_state.last_rerun = time.time()
            time.sleep(1)
            st.rerun()

    st.write(f"### Fill in the {operation.lower()} results")

    user_answers = {}
    correct_count = 0
    total = n * n

    # ✅ Matrix Input Form
    with st.form("matrix_form"):
        # Display column headers
        top_row = st.columns(n + 1)
        top_row[0].markdown("**+**")
        for j, col_val in enumerate(col_nums):
            top_row[j + 1].markdown(f"**{col_val}**")

        # Display input grid
        for i, r in enumerate(row_nums):
            cols = st.columns(n + 1)
            cols[0].markdown(f"**{r}**")
            for j, c in enumerate(col_nums):
                user_input = cols[j + 1].text_input("", key=f"{i}_{j}")
                user_answers[(i, j)] = user_input

        submitted = st.form_submit_button("✅ Submit Answers")

    # ✅ Submission Evaluation
    if submitted:
        elapsed = round(time.time() - st.session_state.start_time, 2)
        st.write("## ✅ Results")

        for i in range(n):
            for j in range(n):
                r = row_nums[i]
                c = col_nums[j]
                user_val = user_answers[(i, j)]
                correct = None

                if operation == "Addition":
                    correct = r + c
                elif operation == "Subtraction":
                    correct = r - c
                elif operation == "Multiplication":
                    correct = r * c

                if user_val.strip().isdigit() and int(user_val.strip()) == correct:
                    correct_count += 1
                    st.success(f"{r} {operation[0]} {c} = {user_val} ✅")
                else:
                    st.error(f"{r} {operation[0]} {c} = {user_val or '?'} ❌ (Correct: {correct})")

        st.info(f"Score: **{correct_count} / {total}**")
        st.info(f"⏱️ Time Taken: **{elapsed} seconds**")
        st.session_state.show_matrix = False

