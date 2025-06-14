import tkinter as tk
from tkinter import ttk
import pyglet

# Colors
COLOR_BG = "#fdfdf5"
COLOR_NAVBAR = "#d6e9d5"
COLOR_SIDEBAR = "#d6e9d5"
COLOR_LINE = "#d3d3d3"
COLOR_CANVAS_BAR = "#fdf6e3"
COLOR_BOX_BORDER = "black"

# Fonts
FONT_BRAND = ("Playfair Display", 20, "bold")
FONT_MENU = ("Playfair Display", 13)
FONT_SECTION = ("Georgia", 16, "bold")
FONT_SUBTEXT = ("Playfair Display", 12)
FONT_AMOUNT = ("Georgia", 24, "underline")
FONT_TRANSACTION = ("Playfair Display", 11)
FONT_BUTTON = ("Arial", 25)
FONT_WELCOME = ("Playfair Display", 22, "bold")

BAR_COLOR = "#fdf6e3"
BAR_FILL_COLOR = "#ffa726"

transactions = [
    ("Food", "-100"),
    ("School Supplies", "-100"),
    ("Emergency Funds", "-100"),
    ("School Fees", "-100"),
    ("General Savings", "-100"),
    ("Personal Goal", "-100"),
    ("Future Purchases", "-100")
]

def draw_rounded_rect(canvas, x, y, w, h, r, color):
    canvas.create_arc(x, y, x + 2*r, y + 2*r, start=90, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2*r, y, x + w, y + 2*r, start=0, extent=90, fill=color, outline=color)
    canvas.create_arc(x, y + h - 2*r, x + 2*r, y + h, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2*r, y + h - 2*r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color)
    canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)

def create_bar(canvas, heights):
    bar_width = 30
    spacing = 15
    x = 15
    max_height = 120
    canvas_height = int(canvas['height'])
    max_value = max(heights) if heights else 1
    for height in heights:
        h = (height / max_value) * max_height if max_value > 0 else 0
        canvas.create_rectangle(x, canvas_height - h - 10, x + bar_width, canvas_height - 10, fill=BAR_FILL_COLOR, outline="")
        x += bar_width + spacing

root = tk.Tk()
root.title("TrackU")
root.geometry("950x520")
root.state("zoomed")
root.configure(bg=COLOR_BG)

root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Sidebar using grid only
sidebar_frame = tk.Frame(root, bg=COLOR_NAVBAR, width=350, highlightthickness=0)
sidebar_frame.grid(row=0, column=0, sticky="nsew")
sidebar_frame.grid_propagate(False)

# Sidebar layout with grid
sidebar_frame.grid_rowconfigure(0, weight=0)
sidebar_frame.grid_rowconfigure(1, weight=0)
sidebar_frame.grid_rowconfigure(2, weight=0)
sidebar_frame.grid_rowconfigure(3, weight=0)
sidebar_frame.grid_rowconfigure(4, weight=0)
sidebar_frame.grid_rowconfigure(5, weight=0)
sidebar_frame.grid_rowconfigure(6, weight=1)  # Pushes content to top

brand_label = tk.Label(sidebar_frame, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
brand_label.grid(row=0, column=0, pady=(20, 30), sticky="ew")

menu_items = ["Dashboard", "Total Expenses", "Total Savings", "", "Profile"]
row = 1
for item in menu_items:
    if item:
        tk.Label(sidebar_frame, text=item, font=FONT_MENU, bg=COLOR_NAVBAR, fg="black").grid(row=row, column=0, pady=10, sticky="ew")
        if item != "Profile":
            tk.Frame(sidebar_frame, bg=COLOR_BOX_BORDER, height=1).grid(row=row+1, column=0, sticky="ew", padx=10)
            row += 1
    else:
        tk.Label(sidebar_frame, text="", bg=COLOR_NAVBAR).grid(row=row, column=0, pady=20)
    row += 1

# Main Content Frame
main_frame = tk.Frame(root, bg=COLOR_BG)
main_frame.grid(row=0, column=1, sticky="nsew", padx=(45, 0), pady=10)
main_frame.grid_columnconfigure(0, weight=1, minsize=1)
main_frame.grid_columnconfigure(1, weight=3)
main_frame.grid_rowconfigure(1, weight=1)

tk.Label(main_frame, text="Welcome, [username]", font=FONT_WELCOME, bg=COLOR_BG).grid(
    row=0, column=0, columnspan=2, sticky="w", padx=(0, 0), pady=(0, 10))

left_frame = tk.Frame(main_frame, bg=COLOR_BG)
left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 0))
left_frame.grid_rowconfigure((0, 1), weight=1)
left_frame.grid_columnconfigure(0, weight=1)

box_titles = ["Total Expenses", "Total Savings"]
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

for i in range(2):
    box_canvas = tk.Canvas(left_frame, width=450, height=300, bg=COLOR_BG, highlightthickness=0)
    box_canvas.grid(row=i, column=0, pady=15, sticky="nsew")
    draw_rounded_rect(box_canvas, 0, 0, 440, 280, 20, COLOR_CANVAS_BAR)
    month_combobox = ttk.Combobox(left_frame, values=months, state="readonly", width=15, font=FONT_SUBTEXT, justify="center")
    month_combobox.current(0)
    box_canvas.create_window(220, 40, window=month_combobox, anchor="center")
    box_canvas.create_text(20, 100, text="₱ 0.00", font=FONT_AMOUNT, fill="black", anchor="w")
    box_canvas.create_text(20, 140, text=box_titles[i], font="Georgia 16 bold", fill="black", anchor="w")
    bar_canvas = tk.Canvas(box_canvas, width=160, height=180, bg=COLOR_CANVAS_BAR, highlightthickness=0)
    box_canvas.create_window(270, 150, window=bar_canvas)
    create_bar(bar_canvas, [30, 60, 90, 120])

right_canvas = tk.Canvas(main_frame, bg=COLOR_BG, highlightthickness=0)
right_canvas.grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=14)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(1, weight=3)

canvas_width = 1000
canvas_height = 500
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