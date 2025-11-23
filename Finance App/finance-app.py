#Imports used for the project

import tkinter as tk
from tkinter import messagebox
import random
import requests

#JSON Fetching from GitHub Repository that I created for questions and tips
def fetch_json(url, key):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json().get(key, [])
    except requests.exceptions.RequestException:
        pass
    return []


questions = fetch_json(
    "https://raw.githubusercontent.com/Erisi357/finance-quiz-data/refs/heads/main/questions.json",
    "questions"
)

tips = fetch_json(
    "https://raw.githubusercontent.com/Erisi357/finance-quiz-data/refs/heads/main/tips.json",
    "tips"
)

random.shuffle(questions)

current_question = 0
score = 0
current_tip = 0

#Start Quiz function which shows a welcome frame when app starts, then includes quiz and tips frame

def start_quiz():
    global score, current_question
    score = 0
    current_question = 0
    welcome_frame.pack_forget()
    tips_frame.pack_forget()
    quiz_frame.pack(fill="both", expand=True)
    score_label.config(text=f"Score: {score}")
    show_question()

#Show question function which shows the questions that are fetched from the GitHub Repository,
#and it's constantly edited when questions change

def show_question():
    global current_question
    if current_question >= len(questions):
        messagebox.showinfo("Quiz finished", f"Your final score: {score}/{len(questions)}")
        root.destroy()
        return

    q=questions[current_question]
    question_label.config(text=q["question"])
    progress_label.config(text=f"Question {current_question + 1} of {len(questions)}")

    opts = q["options"][:]
    random.shuffle(opts)

    for i, text in enumerate(opts):
        option_buttons[i].config(text=text, command=lambda t=text: check_answer(t))
        option_buttons[i].pack(fill="x", pady=5)
    for i in range(len(opts), len(option_buttons)):
        option_buttons[i].pack_forget()

#Check answer function to add points when answer is correct

def check_answer(selected_option):
    global current_question, score
    q = questions[current_question]
    if selected_option == q["answer"]:
        score += 1
    score_label.config(text=f"Score: {score}")
    current_question += 1
    show_question()

#Show tip function which will show the tip frame and remove the welcome frame

def show_tips():
    welcome_frame.pack_forget()
    quiz_frame.pack_forget()
    tips_frame.pack(fill="both", expand=True)
    display_tip()

#Display tip function makes sure to show the tips from the GitHub Repository

def display_tip():
    global current_tip
    if tips:
        tip_label.config(text=tips[current_tip]["tip"])
        tip_progress_label.config(text=f"Tip {current_tip + 1} of {len(tips)}")
    else:
        tip_label.config(text="No tips available.")
        tip_progress_label.config(text="")

#Next tip changes tip to the next one while prev tip changes to previous

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

#Back to welcome brings back to the welcome frame

def back_to_welcome():
    tips_frame.pack_forget()
    quiz_frame.pack_forget()
    welcome_frame.pack(fill="both", expand=True)

#GUI made using Tkinter

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
progress_label.pack(anchor="w", side="top", fill="x", pady=(0, 5), padx=10)

score_label = tk.Label(quiz_frame, text="", font=("Arial", 12))
score_label.pack(anchor="e", fill="x", pady=(0, 10), padx=10)

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