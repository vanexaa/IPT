import tkinter as tk
from tkinter import ttk

# ============================
# Style Configuration Section
# ============================

# Colors
COLOR_BG = "#fdfdf5"
COLOR_NAVBAR = "#ffe0b2"
COLOR_SIDEBAR = "#fdfdf5"
COLOR_LINE = "#d3d3d3"
COLOR_CANVAS_BAR = "#fdf6e3"
COLOR_BOX_BORDER = "black"

# Fonts
FONT_BRAND = ("Georgia", 20, "bold")
FONT_MENU = ("Georgia", 13)
FONT_SECTION = ("Georgia", 14, "bold")
FONT_SUBTEXT = ("Georgia", 12)
FONT_AMOUNT = ("Georgia", 16, "underline")
FONT_TRANSACTION = ("Georgia", 11)
FONT_BUTTON = ("Arial", 16)
FONT_WELCOME = ("Georgia", 12, "bold")

# Chart
BAR_COLOR = "#fdf6e3"

# Sample Transactions
transactions = [
    ("Food", "-100"),
    ("School Supplies", "-100"),
    ("Emergency Funds", "-100"),
    ("School Fees", "-100"),
    ("General Savings", "-100"),
    ("Personal Goal", "-100"),
    ("Future Purchases", "-100")
]


# Create bar chart for spending boxes
def create_bar(canvas, heights):
    canvas.delete("all")
    bar_width = 20
    spacing = 10
    x = 20
    for height in heights:
        canvas.create_rectangle(x, 100 - height, x + bar_width, 100, fill=BAR_COLOR, outline="")
        x += bar_width + spacing


# Toggle Sidebar
def toggle_sidebar():
    if sidebar_frame.winfo_ismapped():
        sidebar_frame.grid_remove()
    else:
        sidebar_frame.grid(row=1, column=0, sticky="ns")


def close_sidebar():
    sidebar_frame.grid_remove()


# Main App Window
root = tk.Tk()
root.title("TrackU")
root.geometry("950x520")
root.state("zoomed")
root.configure(bg=COLOR_BG)

# Configure main layout
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

# Top Navigation Bar
navbar = tk.Frame(root, bg=COLOR_NAVBAR, height=95)
navbar.grid(row=0, column=0, columnspan=2, sticky="nsew")
navbar.grid_propagate(False)
root.grid_rowconfigure(0, minsize=65)

tk.Label(navbar, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR).pack(side="left", padx=20)
tk.Button(navbar, text="≡", font=FONT_BUTTON, bg=COLOR_NAVBAR, bd=0, command=toggle_sidebar).pack(side="right", padx=20)

# Sidebar Frame
sidebar_frame = tk.Frame(root, bg=COLOR_SIDEBAR, width=200, highlightbackground=COLOR_LINE, highlightthickness=1)

tk.Button(sidebar_frame, text="✕", font=FONT_BUTTON, bg=COLOR_NAVBAR, bd=0, command=close_sidebar).pack(anchor="nw", padx=10, pady=10)

for item in ["Dashboard", "Total Expenses", "Total Savings", "", "Profile"]:
    if item:
        tk.Label(sidebar_frame, text=item, font=FONT_MENU, bg=COLOR_SIDEBAR).pack(pady=10)
        if item != "Profile":
            tk.Frame(sidebar_frame, bg=COLOR_BOX_BORDER, height=1).pack(fill="x", padx=10)
    else:
        tk.Label(sidebar_frame, text="", bg=COLOR_SIDEBAR).pack(pady=20)

# Main Content Frame
main_frame = tk.Frame(root, bg=COLOR_BG)
main_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)
main_frame.grid_columnconfigure(1, weight=2)

# Welcome Text
tk.Label(main_frame, text="Welcome, [username]", font=FONT_WELCOME, bg=COLOR_BG).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10))

# Left Section - Spending Boxes
left_frame = tk.Frame(main_frame, bg=COLOR_BG)
left_frame.grid(row=1, column=0, sticky="n", padx=(0, 10))

box_titles = ["Total Expenses", "Total Savings"]
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

for i in range(2):
    box = tk.Frame(left_frame, bg=COLOR_BG, bd=2, relief="groove")
    box.grid(row=i, column=0, pady=10, sticky="ew")

    month_combobox = ttk.Combobox(box, values=months, state="readonly", width=10, font=FONT_SUBTEXT)
    month_combobox.current(0)  # Set default to January
    month_combobox.pack(anchor="w", padx=10, pady=5)

    tk.Label(box, text="₱ 100,000.00", font=FONT_AMOUNT, bg=COLOR_BG).pack(anchor="w", padx=10)
    tk.Label(box, text=box_titles[i], font=FONT_SUBTEXT, bg=COLOR_BG).pack(anchor="w", padx=10, pady=5)

    canvas = tk.Canvas(box, width=200, height=100, bg=COLOR_BG, highlightthickness=0)
    canvas.pack(padx=10, pady=10)
    create_bar(canvas, [20, 40, 60, 80])  # Demo data

# Right Section - Recent Transactions
right_frame = tk.Frame(main_frame, bg=COLOR_BG, bd=2, relief="groove")
right_frame.grid(row=1, column=1, sticky="nsew")

tk.Label(right_frame, text="Recent Transaction", font=FONT_SECTION, bg=COLOR_BG).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 0))
tk.Label(right_frame, text="Category", font=FONT_SUBTEXT, bg=COLOR_BG).grid(row=1, column=0, sticky="w", padx=10)
tk.Label(right_frame, text="Amount", font=FONT_SUBTEXT, bg=COLOR_BG).grid(row=1, column=1, sticky="e", padx=10)

for idx, (category, amount) in enumerate(transactions, start=2):
    tk.Label(right_frame, text=f"• {category}", font=FONT_TRANSACTION, bg=COLOR_BG).grid(row=idx, column=0, sticky="w", padx=20)
    tk.Label(right_frame, text=f"{amount}", font=FONT_TRANSACTION, bg=COLOR_BG).grid(row=idx, column=1, sticky="e", padx=20)

root.mainloop()
