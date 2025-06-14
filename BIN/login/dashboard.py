import tkinter as tk
from tkinter import ttk

# Sample transaction data
transactions = [
    ("Food", "-100"),
    ("School Supplies", "-100"),
    ("Emergency Funds", "-100"),
    ("School Fees", "-100"),
    ("Food", "-100"),
    ("General Savings", "-100"),
    ("Personal Goal", "-100"),
    ("Future Purchases", "-100")
]

# Create main window
root = tk.Tk()
root.title("TrackU")
root.geometry("1000x700")
root.configure(bg="#fffcee")

# Header
header = tk.Frame(root, bg="#f9d9a7", height=60)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header, text="TrackU", font=("Playfair Display", 24, "bold"), bg="#f9d9a7").pack(side="left", padx=20)

# Welcome text
tk.Label(root, text="Welcome, |username|", font=("Playfair Display", 16, "bold"), bg="#fffcee").pack(anchor="w", padx=30, pady=(10, 20))

# Spending section
spending_frame = tk.Frame(root, bg="#fffcee")
spending_frame.pack(padx=30, pady=(0, 20), fill="x")

def create_spending_box(parent):
    frame = tk.Frame(parent, bg="white", highlightbackground="black", highlightthickness=1)
    frame.pack(side="left", padx=10, expand=True, fill="both")

    ttk.Combobox(frame, values=["Month"], state="readonly", width=10).pack(pady=10, padx=10, anchor="w")

    tk.Label(frame, text="₱ 100,000.00", font=("Playfair Display", 20, "underline"), bg="white").pack(anchor="w", padx=10)
    tk.Label(frame, text="Total Spending", font=("Playfair Display", 14), bg="white").pack(anchor="w", padx=10, pady=(0, 10))

    canvas = tk.Canvas(frame, width=100, height=60, bg="white", highlightthickness=0)
    canvas.pack(padx=10, anchor="e")
    bars = [10, 20, 30, 40]
    x = 5
    for h in bars:
        canvas.create_rectangle(x, 60 - h, x + 15, 60, fill="#4b9cd3", outline="")
        x += 20

create_spending_box(spending_frame)
create_spending_box(spending_frame)

# Recent Transactions
trans_frame = tk.Frame(root, bg="white", highlightbackground="black", highlightthickness=1)
trans_frame.pack(padx=30, fill="x")

tk.Label(trans_frame, text="Recent Transaction", font=("Playfair Display", 20, "bold"), bg="white").pack(anchor="w", padx=10, pady=10)

header_row = tk.Frame(trans_frame, bg="white")
header_row.pack(fill="x", padx=10)
tk.Label(header_row, text="Category", font=("Playfair Display", 14, "bold"), bg="white").pack(side="left")
tk.Label(header_row, text="Amount", font=("Playfair Display", 14, "bold"), bg="white").pack(side="right")

for category, amount in transactions:
    row = tk.Frame(trans_frame, bg="white")
    row.pack(fill="x", padx=20)
    tk.Label(row, text=f"• {category}", font=("Playfair Display", 12), bg="white").pack(side="left")
    tk.Label(row, text=amount, font=("Playfair Display", 12), bg="white").pack(side="right")

root.mainloop()
