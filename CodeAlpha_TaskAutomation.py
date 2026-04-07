import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import re
import os
import requests
from datetime import datetime
from urllib.parse import urlparse

# ---------------- GLOBALS ----------------
LOG_FILE = "TaskAutomation_Logs.txt"

# ---------------- FUNCTIONS ----------------
def log_action(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | {message}\n")

def select_folder(entry_widget):
    folder = filedialog.askdirectory()
    if folder:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder)

def select_file(entry_widget):
    file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file)

def run_task():
    task_type = task_var.get()
    try:
        if task_type == "Move JPG Files":
            src = src_entry.get()
            dst = dst_entry.get()
            if not os.path.isdir(src) or not os.path.isdir(dst):
                raise ValueError("Source or Destination folder is invalid!")
            moved = 0
            for file in os.listdir(src):
                if file.lower().endswith(".jpg"):
                    shutil.move(os.path.join(src, file), os.path.join(dst, file))
                    moved += 1
            msg = f"{moved} JPG files moved successfully."
            log_action(msg)
            messagebox.showinfo("Success", msg)

        elif task_type == "Extract Emails from TXT":
            file = file_entry.get()
            if not os.path.isfile(file):
                raise ValueError("Selected file does not exist!")
            with open(file, "r") as f:
                content = f.read()
            emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", content)
            if emails:
                out_file = os.path.join(os.path.dirname(file), "Extracted_Emails.txt")
                with open(out_file, "w") as f:
                    f.write("\n".join(emails))
                msg = f"{len(emails)} emails extracted to {out_file}."
            else:
                msg = "No emails found in the file."
            log_action(msg)
            messagebox.showinfo("Success", msg)

        elif task_type == "Scrape Webpage Title":
            url = url_entry.get()
            if not url.startswith("http"):
                raise ValueError("Please enter a valid URL starting with http/https")
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                raise ValueError(f"Failed to fetch page! Status code: {response.status_code}")
            title_match = re.search(r"<title>(.*?)</title>", response.text, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1).strip() if title_match else "No title found"
            out_file = os.path.join(os.getcwd(), "Webpage_Title.txt")
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(title)
            msg = f"Title saved to {out_file}: {title}"
            log_action(msg)
            messagebox.showinfo("Success", msg)

    except Exception as e:
        log_action(f"Error: {str(e)}")
        messagebox.showerror("Error", str(e))

def clear_fields():
    src_entry.delete(0, tk.END)
    dst_entry.delete(0, tk.END)
    file_entry.delete(0, tk.END)
    url_entry.delete(0, tk.END)

def on_task_change(*args):
    task = task_var.get()
    # Hide all
    src_label.grid_remove()
    src_entry.grid_remove()
    src_btn.grid_remove()
    dst_label.grid_remove()
    dst_entry.grid_remove()
    dst_btn.grid_remove()
    file_label.grid_remove()
    file_entry.grid_remove()
    file_btn.grid_remove()
    url_label.grid_remove()
    url_entry.grid_remove()
    
    if task == "Move JPG Files":
        src_label.grid(row=1, column=0, padx=5, pady=5)
        src_entry.grid(row=1, column=1, padx=5, pady=5)
        src_btn.grid(row=1, column=2, padx=5, pady=5)
        dst_label.grid(row=2, column=0, padx=5, pady=5)
        dst_entry.grid(row=2, column=1, padx=5, pady=5)
        dst_btn.grid(row=2, column=2, padx=5, pady=5)
    elif task == "Extract Emails from TXT":
        file_label.grid(row=1, column=0, padx=5, pady=5)
        file_entry.grid(row=1, column=1, padx=5, pady=5)
        file_btn.grid(row=1, column=2, padx=5, pady=5)
    elif task == "Scrape Webpage Title":
        url_label.grid(row=1, column=0, padx=5, pady=5)
        url_entry.grid(row=1, column=1, padx=5, pady=5)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Extreme Task Automation")
root.geometry("700x400")
root.resizable(False, False)

tk.Label(root, text="Extreme Task Automation", font=("Arial", 22)).pack(pady=10)

task_var = tk.StringVar()
task_var.trace("w", on_task_change)
task_menu = tk.OptionMenu(root, task_var, "Move JPG Files", "Extract Emails from TXT", "Scrape Webpage Title")
task_menu.pack(pady=5)
task_var.set("Move JPG Files")

frame = tk.Frame(root)
frame.pack(pady=10)

# Move JPG widgets
src_label = tk.Label(frame, text="Source Folder:")
src_entry = tk.Entry(frame, width=40)
src_btn = tk.Button(frame, text="Browse", command=lambda: select_folder(src_entry))

dst_label = tk.Label(frame, text="Destination Folder:")
dst_entry = tk.Entry(frame, width=40)
dst_btn = tk.Button(frame, text="Browse", command=lambda: select_folder(dst_entry))

# Extract Emails widgets
file_label = tk.Label(frame, text="TXT File:")
file_entry = tk.Entry(frame, width=40)
file_btn = tk.Button(frame, text="Browse", command=lambda: select_file(file_entry))

# Scrape URL widgets
url_label = tk.Label(frame, text="Webpage URL:")
url_entry = tk.Entry(frame, width=50)

# Buttons
tk.Button(root, text="Run Task", bg="#4CAF50", fg="white", width=15, command=run_task).pack(pady=5)
tk.Button(root, text="Clear Fields", bg="#F44336", fg="white", width=15, command=clear_fields).pack(pady=5)
tk.Button(root, text="Exit", bg="#2196F3", fg="white", width=15, command=root.destroy).pack(pady=5)

# Initialize view
on_task_change()

root.mainloop()
