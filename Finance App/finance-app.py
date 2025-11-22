import tkinter as tk
from tkinter import messagebox
import random
import requests

url_questions = "https://raw.githubusercontent.com/Erisi357/finance-quiz-data/refs/heads/main/questions.json"
response = requests.get(url_questions)
if response.status_code == 200:
    questions = response.json()["questions"]
else:
    questions = []

random.shuffle(questions)

url_tips = "https://raw.githubusercontent.com/Erisi357/finance-quiz-data/refs/heads/main/tips.json"
response = requests.get(url_tips)
if response.status_code == 200:
    tips = response.json()["tips"]
else:
    tips = []

current_question = 0
score = 0
current_tip = 0

def start_quiz():
    welcome_frame.pack_forget()
    tips_frame.pack_forget()
    quiz_frame.pack(fill="both", expand=True)
    show_question()

def show_question():
    global current_question
    if current_question < len(questions):
        q = questions[current_question]
        question_label.config(text=q["question"])
        progress_label.config(text=f"Question {current_question + 1} of {len(questions)}")
        options = q["options"].copy()
        random.shuffle(options)
        for i, option_text in enumerate(options):
            if i < len(option_buttons):
                option_buttons[i].config(text=option_text, command=lambda opt=option_text: check_answer(opt))
                option_buttons[i].pack(fill="x", pady=5)
        for i in range(len(options), len(option_buttons)):
            option_buttons[i].pack_forget()
    else:
        messagebox.showinfo("Quiz Finished", f"Your final score: {score}/{len(questions)}")
        root.destroy()

def check_answer(selected_option):
    global current_question, score
    q = questions[current_question]
    if selected_option == q["answer"]:
        score += 1
    score_label.config(text=f"Score: {score}")
    current_question += 1
    show_question()

def show_tips():
    welcome_frame.pack_forget()
    quiz_frame.pack_forget()
    tips_frame.pack(fill="both", expand=True)
    display_tip()

def display_tip():
    global current_tip
    if tips:
        tip_label.config(text=tips[current_tip]["tip"])
        tip_progress_label.config(text=f"Tip {current_tip + 1} of {len(tips)}")
    else:
        tip_label.config(text="No tips available.")
        tip_progress_label.config(text="")

def next_tip():
    global current_tip
    if current_tip < len(tips) - 1:
        current_tip += 1
        display_tip()

def prev_tip():
    global current_tip
    if current_tip > 0:
        current_tip -= 1
        display_tip()

def back_to_welcome():
    tips_frame.pack_forget()
    quiz_frame.pack_forget()
    welcome_frame.pack(fill="both", expand=True)

root = tk.Tk()
root.title("Fun Finance App")
root.geometry("550x450")
root.resizable(False, False)

welcome_frame = tk.Frame(root, padx=20, pady=20)
welcome_frame.pack(fill="both", expand=True)

welcome_label = tk.Label(welcome_frame, text="Welcome to Fun Finance", font=("Arial", 22))
welcome_label.pack(pady=(60, 30))

start_button = tk.Button(welcome_frame, text="Start Quiz", font=("Arial", 14), width=20, height=2, command=start_quiz)
start_button.pack(pady=(0, 15))

tips_button = tk.Button(welcome_frame, text="Tips", font=("Arial", 14), width=20, height=2, command=show_tips)
tips_button.pack()

quiz_frame = tk.Frame(root, padx=20, pady=20)

progress_label = tk.Label(quiz_frame, text="", font=("Arial", 12))
progress_label.pack(anchor="nw", pady=(0, 5), padx=10)

score_label = tk.Label(quiz_frame, text="", font=("Arial", 12))
score_label.pack(anchor="nw", pady=(0, 10), padx=10)

question_label = tk.Label(quiz_frame, text="", wraplength=500, font=("Arial", 16), justify="left")
question_label.pack(fill="x", pady=(0, 20))

option_buttons = []
for _ in range(4):
    btn = tk.Button(
        quiz_frame,
        text="",
        font=("Arial", 13),
        wraplength=500,
        justify="left",
        anchor="w",
        padx=10
    )
    btn.pack(fill="x", pady=5)
    option_buttons.append(btn)

tips_frame = tk.Frame(root, padx=20, pady=20)

tip_progress_label = tk.Label(tips_frame, text="", font=("Arial", 12))
tip_progress_label.pack(anchor="e", pady=(0, 10), padx=10)

tip_label = tk.Label(tips_frame, text="", font=("Arial", 15), wraplength=500, justify="left")
tip_label.pack(fill="x", pady=(0, 20))

nav_frame = tk.Frame(tips_frame)
nav_frame.pack(fill="x", pady=10)

prev_button = tk.Button(nav_frame, text="Previous", font=("Arial", 12), command=prev_tip)
prev_button.pack(side="left", expand=True, fill="x", padx=5)

next_button = tk.Button(nav_frame, text="Next", font=("Arial", 12), command=next_tip)
next_button.pack(side="left", expand=True, fill="x", padx=5)

back_button = tk.Button(tips_frame, text="Back", font=("Arial", 12), command=back_to_welcome)
back_button.pack(fill="x", pady=(10, 0))

back_button = tk.Button(quiz_frame, text="Back", font=("Arial", 12), command=back_to_welcome)
back_button.pack(fill="x", pady=(10, 0))

root.mainloop()