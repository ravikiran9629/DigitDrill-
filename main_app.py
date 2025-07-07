import streamlit as st
import random
import time

# -------------------
# Page Setup
# -------------------
st.set_page_config(page_title="Matrix Math Practice", layout="centered")
st.title("🧠 Matrix Math Practice App")

# -------------------
# Select Operation First
# -------------------
operation = st.selectbox("🔧 Select Operation", ["Addition", "Subtraction", "Multiplication", "Division"])

# -------------------
# Difficulty Options Based on Operation
# -------------------
if operation == "Division":
    level_options = ["🔴 Hard"]
elif operation == "Multiplication":
    level_options = ["🟡 Medium", "🔴 Hard"]
else:
    level_options = ["🟢 Easy", "🟡 Medium", "🔴 Hard"]

level = st.radio("🎮 Choose Difficulty Level", level_options, horizontal=True)

# -------------------
# Valid Digit Options Based on Operation & Level
# -------------------
def get_digit_options(operation, level):
    if operation in ["Addition", "Subtraction"]:
        return [1, 2] if level == "🟢 Easy" else [2, 3] if level == "🟡 Medium" else [3, 4]
    elif operation == "Multiplication":
        return [1, 2] if level == "🟡 Medium" else [2, 3, 4]
    else:  # Division
        return [1, 2]

digit_options = get_digit_options(operation, level)

# -------------------
# Matrix Size and Digit Selection
# -------------------
n = st.slider("Select Matrix Size (n x n)", 2, 10, 5)
digits_row = st.selectbox("Digits for Row Numbers", digit_options)
digits_col = st.selectbox("Digits for Column Numbers", digit_options)

# -------------------
# Generate Number Range Based on Difficulty
# -------------------
def generate_numbers(n, digits, level):
    full_min = 10 ** (digits - 1)
    full_max = (10 ** digits) - 1
    total_range = full_max - full_min + 1
    chunk = total_range // 3

    if level.startswith("🟢"):
        min_val = full_min
        max_val = full_min + chunk - 1
    elif level.startswith("🟡"):
        min_val = full_min + chunk
        max_val = full_min + 2 * chunk - 1
    else:
        min_val = full_min + 2 * chunk
        max_val = full_max

    if max_val - min_val + 1 < n:
        raise ValueError(
            f"Not enough unique numbers in range {min_val}-{max_val} for {n} values. "
            f"Try reducing matrix size or changing level/digits."
        )

    return random.sample(range(min_val, max_val + 1), n)

# -------------------
# Session State Setup
# -------------------
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "show_matrix" not in st.session_state:
    st.session_state.show_matrix = False

# -------------------
# Generate Button
# -------------------
if st.button("🌀 Generate Matrix"):
    try:
        st.session_state.col_nums = generate_numbers(n, digits_col, level)
        st.session_state.row_nums = generate_numbers(n, digits_row, level)
        st.session_state.start_time = time.time()
        st.session_state.show_matrix = True
    except ValueError as e:
        st.error(str(e))

# -------------------
# Show Matrix and Input Form
# -------------------
if st.session_state.get("show_matrix", False):
    col_nums = st.session_state.col_nums
    row_nums = st.session_state.row_nums
    symbol = {"Addition": "+", "Subtraction": "-", "Multiplication": "×", "Division": "÷"}[operation]
    st.markdown(f"### Fill in the answers ({level})")
    st.markdown(f"➡️ **Each cell = Column {symbol} Row**")


    user_answers = {}
    correct_count = 0
    total = n * n

    with st.form("matrix_form"):
        # Header row
        top_row = st.columns(n + 1)
        top_row[0].markdown("**↘️**")
        for j, col_val in enumerate(col_nums):
            top_row[j + 1].markdown(f"**{col_val}**")

        # Input matrix
        for i, r in enumerate(row_nums):
            cols = st.columns(n + 1)
            cols[0].markdown(f"**{r}**")
            for j, c in enumerate(col_nums):
                user_input = cols[j + 1].text_input("", key=f"{i}_{j}")
                user_answers[(i, j)] = user_input

        submitted = st.form_submit_button("✅ Submit Answers")

    # -------------------
    # Evaluate
    # -------------------
    if submitted:
        elapsed = round(time.time() - st.session_state.start_time, 2)
        st.write("## ✅ Results")

        for i in range(n):
            for j in range(n):
                r = row_nums[i]
                c = col_nums[j]
                user_val = user_answers[(i, j)]
                correct = None

                try:
                    if operation == "Addition":
                        correct = r + c
                    elif operation == "Subtraction":
                        correct = r - c
                    elif operation == "Multiplication":
                        correct = r * c
                    elif operation == "Division":
                        correct = round(r / c, 2) if c != 0 else None

                    if operation != "Division":
                        is_correct = user_val.strip().isdigit() and int(user_val.strip()) == correct
                    else:
                        is_correct = (
                            user_val.strip().replace('.', '', 1).isdigit() and
                            abs(float(user_val.strip()) - correct) < 0.01
                        )

                    if is_correct:
                        correct_count += 1
                        st.success(f"{r} {operation[0]} {c} = {user_val} ✅")
                    else:
                        st.error(f"{r} {operation[0]} {c} = {user_val or '?'} ❌ (Correct: {correct})")

                except:
                    st.error(f"{r} {operation[0]} {c} = {user_val or '?'} ❌ (Invalid Input)")

        st.info(f"🎯 Score: **{correct_count} / {total}**")
        st.info(f"🕒 Time Taken: **{elapsed} seconds**")
        st.session_state.show_matrix = False



