Matrix Math Practice App
An interactive app built with Streamlit to practice arithmetic operations in a matrix format.
Great for improving mental math speed — especially for competitive exam prep or school-level drills.

🚀 Features
✅ Select operation: Addition, Subtraction, Multiplication, Division
✅ Choose difficulty level: 🟢 Easy, 🟡 Medium, 🔴 Hard
✅ Customize digits for row and column numbers
✅ Set your preferred matrix size (n × n)
✅ Smart number generation (non-repeating, level-based)
✅ User inputs answers into a matrix form
✅ Real-time feedback: ✅ for correct, ❌ for incorrect
✅ Score and time taken shown after submission
✅ Clear instructions like: Each cell = Column op Row

🛠️ Tech Stack
Python 3.x

Streamlit

Built-in libraries: random, time

▶️ How to Run the App
bash
Copy
Edit
# Step 1: Install Streamlit
pip install streamlit

# Step 2: Run the app
streamlit run app.py
💡 How Difficulty Is Determined
Difficulty is based on the calculation complexity, not the user's level.

🔢 Number Range Generation
Based on selected digit count:

1-digit → 1 to 9

2-digit → 10 to 99

3-digit → 100 to 999

Then the range is divided into 3 parts:

🟢 Easy → Lower third (e.g., 10–39 for 2-digit)

🟡 Medium → Middle third (e.g., 40–69)

🔴 Hard → Upper third (e.g., 70–99)

This controls how small or large the numbers are in each cell.

🎯 Operation + Digit Combo Logic
Each operation has its own difficulty based on how "mentally heavy" the math is.

➕ Addition / ➖ Subtraction
Level	Allowed Digits
🟢 Easy	1–2 digits
🟡 Medium	2–3 digits
🔴 Hard	3–4 digits

✖️ Multiplication
Level	Allowed Digit Combos (Row × Col)
🟢 Easy	1×1, 1×2, 2×1
🟡 Medium	2×2, 2×3, 3×2
🔴 Hard	3×3, 3×4, 4×4

➗ Division (Row ÷ Col)
Level	Allowed Digit Combos
🟢 Easy	1÷1, 2÷1, 1÷2 (clean)
🔴 Hard	2÷2, 3÷1, 4÷2, etc.
🟡 Medium	🔒 Not implemented

🔹 “Clean” division = whole number answers only
🔹 Hard division answers are rounded to 2 decimal places

📐 Matrix Size
Matrix size (n × n) is chosen via a slider (2–10).

In the future, it may auto-limit based on difficulty & operation (e.g., Hard Division → max 5×5)

📋 Sample Flow
Select Operation: e.g., Multiplication

Choose Difficulty: 🟢 Easy

Set digits: Rows = 1, Columns = 2

Matrix size: 3 × 3

Click Generate Matrix

Fill in answers → Submit

Review results, score, and time

🧪 Planned Improvements
 🚫 Block invalid digit combos in Easy mode

 📏 Auto-limit matrix size based on difficulty

 🔀 Option to choose Row op Column vs Column op Row

 🕒 Optional live timer toggle

 📊 Track and visualize performance over time

 ⬇️ Export answers and scores to CSV

 📱 Mobile responsiveness fixes

 📦 Streamlit Cloud deployment / .exe export

