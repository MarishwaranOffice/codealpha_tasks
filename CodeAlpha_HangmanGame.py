import tkinter as tk
from tkinter import messagebox
import random
import datetime

# ---------------- CONFIG ----------------
WORDS = {
    "Easy": ["apple", "tiger", "chair", "bread", "plant"],
    "Medium": ["elephant", "dolphin", "mountain", "computer", "notebook"],
    "Hard": ["encyclopedia", "hippopotamus", "transformation", "architecture", "psychology"]
}
MAX_TRIES = 6
TIMER_SECONDS = 60
RESULTS_FILE = "Hangman_Game_Results.txt"
HINTS_ALLOWED = 1

# ---------------- GLOBALS ----------------
word = ""
display = []
guessed_letters = []
tries = MAX_TRIES
time_left = TIMER_SECONDS
timer_id = None
hints_used = 0
score = {"Wins": 0, "Losses": 0, "TimeUp": 0}

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Ultimate Hangman Game")
root.geometry("750x700")
root.resizable(False, False)

# ---------------- CANVAS ----------------
canvas = tk.Canvas(root, width=200, height=250, bg="#f0f0f0")
canvas.pack(pady=10)

def draw_stand():
    canvas.create_line(20, 230, 180, 230)   # base
    canvas.create_line(50, 230, 50, 20)     # pole
    canvas.create_line(50, 20, 120, 20)     # top
    canvas.create_line(120, 20, 120, 40)    # rope

draw_stand()

# ---------------- LABELS ----------------
word_label = tk.Label(root, text="", font=("Arial", 28))
word_label.pack(pady=10)

tries_label = tk.Label(root, text=f"Tries Left: {MAX_TRIES}", font=("Arial", 14))
tries_label.pack()

timer_label = tk.Label(root, text=f"Time Left: {TIMER_SECONDS}s", font=("Arial", 14))
timer_label.pack()

msg_label = tk.Label(root, text="", font=("Arial", 14))
msg_label.pack(pady=10)

score_label = tk.Label(root, text="Score - Wins:0 | Losses:0 | TimeUp:0", font=("Arial", 12))
score_label.pack(pady=5)

# ---------------- FUNCTIONS ----------------
def start_game(difficulty):
    global word, display, guessed_letters, tries, time_left, timer_id, hints_used
    stop_timer()
    canvas.delete("all")
    draw_stand()

    word = random.choice(WORDS[difficulty]).lower()
    display = ["_"] * len(word)
    guessed_letters = []
    tries = MAX_TRIES
    time_left = TIMER_SECONDS
    hints_used = 0

    word_label.config(text=" ".join(display))
    tries_label.config(text=f"Tries Left: {tries}")
    msg_label.config(text="")

    for b in buttons:
        b.config(state="normal")

    countdown()

def draw_part():
    parts = MAX_TRIES - tries
    if parts == 1:
        canvas.create_oval(100, 40, 140, 80)  # head
    elif parts == 2:
        canvas.create_line(120, 80, 120, 140)  # body
    elif parts == 3:
        canvas.create_line(120, 100, 90, 120)  # left arm
    elif parts == 4:
        canvas.create_line(120, 100, 150, 120)  # right arm
    elif parts == 5:
        canvas.create_line(120, 140, 90, 180)  # left leg
    elif parts == 6:
        canvas.create_line(120, 140, 150, 180)  # right leg

def check(letter):
    global tries
    if letter in guessed_letters:
        msg_label.config(text=f"Already guessed '{letter}'")
        return
    guessed_letters.append(letter)

    if letter in word:
        msg_label.config(text=f"Correct! '{letter}'")
        for i, l in enumerate(word):
            if l == letter:
                display[i] = letter
    else:
        tries -= 1
        msg_label.config(text=f"Wrong! '{letter}' is not in the word.")
        draw_part()

    word_label.config(text=" ".join(display))
    tries_label.config(text=f"Tries Left: {tries}")

    if "_" not in display:
        msg_label.config(text="🎉 You Win! 🎉")
        update_score("Wins")
        save_result("WIN")
        disable_buttons()
        stop_timer()
    elif tries == 0:
        msg_label.config(text=f"💀 You Lost! Word was '{word}' 💀")
        update_score("Losses")
        save_result("LOSE")
        disable_buttons()
        stop_timer()

def use_hint():
    global hints_used
    if hints_used >= HINTS_ALLOWED:
        msg_label.config(text="No hints left!")
        return
    available_indices = [i for i, l in enumerate(display) if l == "_"]
    if available_indices:
        index = random.choice(available_indices)
        display[index] = word[index]
        word_label.config(text=" ".join(display))
        hints_used += 1
        msg_label.config(text=f"Hint used! Revealed 1 letter.")
    if "_" not in display:
        msg_label.config(text="🎉 You Win! 🎉")
        update_score("Wins")
        save_result("WIN")
        disable_buttons()
        stop_timer()

def disable_buttons():
    for b in buttons:
        b.config(state="disabled")

def countdown():
    global time_left, timer_id
    timer_label.config(text=f"Time Left: {time_left}s")
    if time_left > 0:
        time_left -= 1
        timer_id = root.after(1000, countdown)
    else:
        msg_label.config(text=f"⏰ Time Up! Word was '{word}'")
        update_score("TimeUp")
        save_result("TIME UP")
        disable_buttons()

def stop_timer():
    global timer_id
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None

def save_result(status):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(RESULTS_FILE, "a") as f:
        f.write(f"{now} | Word: {word} | Status: {status}\n")

def update_score(result_type):
    score[result_type] += 1
    score_label.config(text=f"Score - Wins:{score['Wins']} | Losses:{score['Losses']} | TimeUp:{score['TimeUp']}")

# ---------------- LETTER BUTTONS ----------------
frame = tk.Frame(root)
frame.pack(pady=10)

letters = "abcdefghijklmnopqrstuvwxyz"
buttons = []
for i, letter in enumerate(letters):
    btn = tk.Button(frame, text=letter.upper(), width=4, font=("Arial", 10),
                    command=lambda l=letter: check(l))
    btn.grid(row=i//9, column=i%9, padx=2, pady=2)
    buttons.append(btn)

# ---------------- HINT BUTTON ----------------
tk.Button(root, text="Use Hint", bg="#FF9800", fg="white", font=("Arial", 12),
          command=use_hint).pack(pady=5)

# ---------------- DIFFICULTY BUTTONS ----------------
tk.Label(root, text="Select Difficulty:", font=("Arial", 12)).pack(pady=5)
diff_frame = tk.Frame(root)
diff_frame.pack(pady=5)
for diff in ["Easy", "Medium", "Hard"]:
    tk.Button(diff_frame, text=diff, width=10, font=("Arial", 10),
              command=lambda d=diff: start_game(d)).pack(side="left", padx=5)

# ---------------- RESTART BUTTON ----------------
tk.Button(root, text="Restart Game", bg="#4CAF50", fg="white", font=("Arial", 12),
          command=lambda: start_game("Easy")).pack(pady=10)

# ---------------- START GAME ----------------
start_game("Easy")
root.mainloop()
