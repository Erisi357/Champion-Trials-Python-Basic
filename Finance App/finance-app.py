import tkinter as tk
from tkinter import messagebox
import random
import requests

url_questions = "https://raw.githubusercontent.com/Erisi357/finance-quiz-data/refs/heads/main/questions.json"
response = requests.get(url_questions)
if response.status_code == 200:
    questions = response.json()["questions"]
else:
    print("Failed to get questions")
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
        options = q["options"].copy()
        random.shuffle(options)
        for i, option_text in enumerate(options):
            option_buttons[i].config(
                text=option_text,
                command=lambda opt=option_text: check_answer(opt)
            )
    else:
        messagebox.showinfo("Quiz Finished", f"Your final score: {score}/{len(questions)}")
        root.destroy()

def check_answer(selected_option):
    global current_question, score
    q = questions[current_question]
    if selected_option == q["answer"]:
        score += 1
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
    else:
        tip_label.config(text="No tips available.")

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
root.title("Finance Quiz")
root.geometry("600x500")
root.resizable(False, False)

welcome_frame = tk.Frame(root)
welcome_frame.pack(fill="both", expand=True)

welcome_label = tk.Label(welcome_frame, text="Welcome to the Finance Quiz!", font=("Arial", 20))
welcome_label.pack(pady=40)

start_button = tk.Button(welcome_frame, text="Start Quiz", font=("Arial", 14), width=20, height=2, command=start_quiz)
start_button.pack(pady=(0,15))

tips_button = tk.Button(welcome_frame, text="Tips", font=("Arial", 14), width=20, height=2, command=show_tips)
tips_button.pack()

tips_frame = tk.Frame(root)

tip_label = tk.Label(tips_frame, text="", font=("Arial", 14), wraplength=550, justify="left")
tip_label.pack(pady=40, padx=20)

nav_frame = tk.Frame(tips_frame)
nav_frame.pack(pady=20)

prev_button = tk.Button(nav_frame, text="Previous", font=("Arial", 12), width=12, command=prev_tip)
prev_button.pack(side="left", padx=10)

next_button = tk.Button(nav_frame, text="Next", font=("Arial", 12), width=12, command=next_tip)
next_button.pack(side="left", padx=10)

back_button = tk.Button(tips_frame, text="Back", font=("Arial", 12), width=15, command=back_to_welcome)
back_button.pack(pady=10)

quiz_frame = tk.Frame(root)

question_label = tk.Label(quiz_frame, text="", wraplength=550, font=("Arial", 16), justify="left")
question_label.pack(pady=40)

option_buttons = []
for _ in range(4):
    btn = tk.Button(quiz_frame, text="", width=50, height=2, font=("Arial", 12))
    btn.pack(pady=10)
    option_buttons.append(btn)

root.mainloop()
