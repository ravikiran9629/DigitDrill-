import streamlit as st
import random
import time
from datetime import timedelta


# Function to generate random numbers with given digits
def generate_numbers(n, digits):
    min_val = 10**(digits - 1)
    max_val = (10**digits) - 1
    return [random.randint(min_val, max_val) for _ in range(n)]

# Header
st.title("🧮 Matrix Calculation Practice")

# Inputs
n = st.slider("Matrix size (n x n)", 2, 10, 5)
digits_col = st.number_input("Digits for Column Numbers", 1, 5, 2)
digits_row = st.number_input("Digits for Row Numbers", 1, 5, 2)
operation = st.selectbox("Choose Operation", ["Addition", "Subtraction", "Multiplication"])

if "start_time" not in st.session_state:
    st.session_state.start_time = None

# Timer placeholder
timer_placeholder = st.empty()


if st.button("🌀 Generate Matrix"):
    col_nums = generate_numbers(n, digits_col)
    row_nums = generate_numbers(n, digits_row)
    st.session_state.col_nums = col_nums
    st.session_state.row_nums = row_nums
    st.session_state.start_time = time.time()
    st.session_state.show_matrix = True

if st.session_state.get("show_matrix", False):
    # Show header
    st.write(f"### Fill in the {operation.lower()} results")
    col_nums = st.session_state.col_nums
    row_nums = st.session_state.row_nums

    # ✅ Live Timer Logic
if st.session_state.start_time:
        elapsed = int(time.time() - st.session_state.start_time)
        timer_placeholder.markdown(
            f"<div style='position: fixed; top: 10px; right: 20px; background-color: #f0f0f0; "
            f"padding: 10px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);'>"
            f"<strong>⏱️ Time Elapsed: {elapsed} sec</strong></div>",
            unsafe_allow_html=True
        )
        time.sleep(1)
        st.experimental_rerun()

    user_answers = {}
    correct_count = 0
    total = n * n

    with st.form("matrix_form"):
    # Display column headers
    top_row = st.columns(n + 1)
    top_row[0].markdown("**+**")  # Top-left empty cell
    for j, col_val in enumerate(col_nums):
        top_row[j + 1].markdown(f"**{col_val}**")

    # Now display the rows
    for i, r in enumerate(row_nums):
        cols = st.columns(n + 1)
        cols[0].markdown(f"**{r}**")  # Row label
        for j, c in enumerate(col_nums):
            user_input = cols[j + 1].text_input("", key=f"{i}_{j}")
            user_answers[(i, j)] = user_input

    submitted = st.form_submit_button("✅ Submit Answers")


    if submitted:
        elapsed = round(time.time() - st.session_state.start_time, 2)
        st.write("## ✅ Results")

        for i in range(n):
            for j in range(n):
                r, c = row_nums[i], col_nums[j]
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
