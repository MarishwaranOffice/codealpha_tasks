import tkinter as tk
from tkinter import messagebox
import datetime
import csv

# ---------------- CONFIG ----------------
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 2800,
    "AMZN": 3500,
    "MSFT": 300,
    "NFLX": 500,
    "META": 220
}

RESULTS_FILE = "Stock_Portfolio_Results.csv"

# ---------------- GLOBALS ----------------
portfolio = {}

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Ultimate Stock Portfolio Tracker")
root.geometry("700x600")
root.resizable(False, False)

# ---------------- FUNCTIONS ----------------
def add_stock():
    stock = stock_entry.get().upper()
    qty = qty_entry.get()
    if stock not in STOCK_PRICES:
        messagebox.showerror("Error", f"{stock} is not in our stock list!")
        return
    if not qty.isdigit() or int(qty) <= 0:
        messagebox.showerror("Error", "Quantity must be a positive integer!")
        return

    qty = int(qty)
    if stock in portfolio:
        portfolio[stock] += qty
    else:
        portfolio[stock] = qty

    stock_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    update_portfolio_display()

def update_portfolio_display():
    display_text = ""
    total_value = 0
    for stock, qty in portfolio.items():
        price = STOCK_PRICES[stock]
        value = price * qty
        display_text += f"{stock}: {qty} shares × ${price} = ${value}\n"
        total_value += value
    portfolio_label.config(text=display_text)
    total_label.config(text=f"Total Investment Value: ${total_value}")
    
def save_portfolio():
    if not portfolio:
        messagebox.showinfo("Info", "Portfolio is empty!")
        return
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(RESULTS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        for stock, qty in portfolio.items():
            writer.writerow([now, stock, qty, STOCK_PRICES[stock], STOCK_PRICES[stock]*qty])
    messagebox.showinfo("Saved", f"Portfolio saved to {RESULTS_FILE}")

def clear_portfolio():
    global portfolio
    portfolio = {}
    update_portfolio_display()

# ---------------- GUI ELEMENTS ----------------
tk.Label(root, text="Ultimate Stock Portfolio Tracker", font=("Arial", 22)).pack(pady=10)

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Stock Symbol:").grid(row=0, column=0, padx=5, pady=5)
stock_entry = tk.Entry(input_frame, width=10)
stock_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Quantity:").grid(row=0, column=2, padx=5, pady=5)
qty_entry = tk.Entry(input_frame, width=10)
qty_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Button(input_frame, text="Add Stock", bg="#4CAF50", fg="white", width=12, command=add_stock).grid(row=0, column=4, padx=5)

# Portfolio display
portfolio_label = tk.Label(root, text="", font=("Arial", 14), justify="left")
portfolio_label.pack(pady=10)

total_label = tk.Label(root, text="Total Investment Value: $0", font=("Arial", 16, "bold"))
total_label.pack(pady=5)

# Action buttons
action_frame = tk.Frame(root)
action_frame.pack(pady=10)

tk.Button(action_frame, text="Save Portfolio", bg="#2196F3", fg="white", width=15, command=save_portfolio).grid(row=0, column=0, padx=10)
tk.Button(action_frame, text="Clear Portfolio", bg="#F44336", fg="white", width=15, command=clear_portfolio).grid(row=0, column=1, padx=10)

# ---------------- START APP ----------------
root.mainloop()
