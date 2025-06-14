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
FONT_SECTION = ("Georgia", 16, "bold")  # bigger for titles inside boxes
FONT_SUBTEXT = ("Georgia", 12)
FONT_AMOUNT = ("Georgia", 24, "underline")  # bigger for amounts
FONT_TRANSACTION = ("Georgia", 11)
FONT_BUTTON = ("Arial", 16)
FONT_WELCOME = ("Georgia", 12, "bold")

# Chart
BAR_COLOR = "#fdf6e3"
BAR_FILL_COLOR = "#ffa726"  # A visible orange color for bars

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

# Function to draw rounded rectangle
def draw_rounded_rect(canvas, x, y, w, h, r, color):
    canvas.create_arc(x, y, x + 2*r, y + 2*r, start=90, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2*r, y, x + w, y + 2*r, start=0, extent=90, fill=color, outline=color)
    canvas.create_arc(x, y + h - 2*r, x + 2*r, y + h, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2*r, y + h - 2*r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color)
    canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)

# Create bar chart for spending boxes
def create_bar(canvas, heights):
    bar_width = 30
    spacing = 15
    x = 15
    max_height = 120
    canvas_height = int(canvas['height'])
    max_value = max(heights) if heights else 1
    for height in heights:
        # Normalize height to max_height
        h = (height / max_value) * max_height if max_value > 0 else 0
        # Draw bar from bottom up
        canvas.create_rectangle(x, canvas_height - h - 10, x + bar_width, canvas_height - 10, fill=BAR_FILL_COLOR, outline="")
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
root.grid_columnconfigure(1, weight=3)  # Right side expands more
root.grid_columnconfigure(0, weight=1)  # Sidebar column smaller
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
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=3)
main_frame.grid_rowconfigure(1, weight=1)

# Welcome Text
tk.Label(main_frame, text="Welcome, [username]", font=FONT_WELCOME, bg=COLOR_BG).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10))

# Left Section - Spending Boxes (Total Expenses & Total Savings)
left_frame = tk.Frame(main_frame, bg=COLOR_BG)
left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
left_frame.grid_rowconfigure((0,1), weight=1)
left_frame.grid_columnconfigure(0, weight=1)

box_titles = ["Total Expenses", "Total Savings"]
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

for i in range(2):
    box_canvas = tk.Canvas(left_frame, width=350, height=300, bg=COLOR_BG, highlightthickness=0)
    box_canvas.grid(row=i, column=0, pady=15, sticky="nsew")

    draw_rounded_rect(box_canvas, 0, 0, 450, 300, 20, COLOR_CANVAS_BAR)

    # Left side texts & combobox - around x=100
    month_combobox = ttk.Combobox(left_frame, values=months, state="readonly", width=15, font=FONT_SUBTEXT)
    month_combobox.current(0)
    box_canvas.create_window(100, 70, window=month_combobox)

    box_canvas.create_text(100, 130, text="₱ 0.00", font=FONT_AMOUNT, fill="black")
    box_canvas.create_text(100, 170, text=box_titles[i], font=FONT_SECTION, fill="black")

    # Right side bar canvas
    bar_canvas = tk.Canvas(box_canvas, width=160, height=220, bg=COLOR_CANVAS_BAR, highlightthickness=0)
    box_canvas.create_window(270, 150, window=bar_canvas)  # right half, vertically centered

    # Sample bar heights, bars drawn side by side horizontally
    create_bar(bar_canvas, [30, 60, 90, 120])





# Right Section - Recent Transactions (bigger)
right_canvas = tk.Canvas(main_frame, bg=COLOR_BG, highlightthickness=0)
right_canvas.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(1, weight=3)

# Draw background rounded rect to fill right side
canvas_width = 600
canvas_height = 450
right_canvas.config(width=canvas_width, height=canvas_height)
draw_rounded_rect(right_canvas, 0, 0, canvas_width, canvas_height, 20, COLOR_CANVAS_BAR)

right_canvas.create_text(20, 20, anchor="nw", text="Recent Transaction", font=FONT_SECTION, fill="black")
right_canvas.create_text(20, 60, anchor="nw", text="Category", font=FONT_SUBTEXT, fill="black")
right_canvas.create_text(canvas_width - 30, 60, anchor="ne", text="Amount", font=FONT_SUBTEXT, fill="black")

y_offset = 100
line_height = 28
for idx, (category, amount) in enumerate(transactions):
    right_canvas.create_text(30, y_offset, anchor="w", text=f"• {category}", font=FONT_TRANSACTION, fill="black")
    right_canvas.create_text(canvas_width - 30, y_offset, anchor="e", text=f"{amount}", font=FONT_TRANSACTION, fill="black")
    y_offset += line_height

root.mainloop()
