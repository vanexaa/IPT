import tkinter as tk
from tkinter import ttk
import pyglet

# Colors
COLOR_BG = "#fdfdf5"
COLOR_NAVBAR = "#ffe0b2"  # Navbar color
COLOR_SIDEBAR = "#d6e9d5"  # Sidebar color
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


# Function to draw a rectangle with only bottom corners rounded
def draw_bottom_rounded_rect(canvas, x, y, w, h, r, color):
    # Top straight line
    canvas.create_rectangle(x, y, x + w, y + r, fill=color, outline=color)
    # Middle straight part
    canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)
    # Bottom arcs (rounded corners)
    canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
    # Connect the arcs with a straight line at the bottom
    canvas.create_rectangle(x + r, y + h - r, x + w - r, y + h, fill=color, outline=color)


# Function to draw rounded rectangle (for general use where all 4 corners are rounded)
def draw_rounded_rect(canvas, x, y, w, h, r, color):
    canvas.create_arc(x, y, x + 2 * r, y + 2 * r, start=90, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y, x + w, y + 2 * r, start=0, extent=90, fill=color, outline=color)
    canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color)
    canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)


def create_bar(canvas, heights):
    canvas.delete("bar")  # Clear existing bars
    bar_width = 30
    spacing = 15
    x = 15
    max_height = 120  # Max bar height
    canvas_height = int(canvas.winfo_height()) if canvas.winfo_height() > 1 else 180  # Get current canvas height
    max_value = max(heights) if heights else 1

    for height in heights:
        h = (height / max_value) * max_height if max_value > 0 else 0
        # Draw bar from bottom up, adjusting for padding
        canvas.create_rectangle(x, canvas_height - h - 10, x + bar_width, canvas_height - 10, fill=BAR_FILL_COLOR,
                                outline="", tags="bar")
        x += bar_width + spacing


# --- Functions to draw/update box content on resize ---

def update_left_box_canvas(event, box_canvas, month_combobox, title_text, amount_text, bar_canvas):
    box_canvas.delete("all")
    current_width = event.width
    current_height = event.height

    # Draw the main rounded rectangle background
    draw_rounded_rect(box_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR)

    # Position month combobox (centered horizontally, near top)
    box_canvas.create_window(current_width / 2, 40, window=month_combobox, anchor="center")

    # Position amount and title texts (aligned to left)
    box_canvas.create_text(20, 100, text=amount_text, font=FONT_AMOUNT, fill="black", anchor="w")
    box_canvas.create_text(20, 140, text=title_text, font=FONT_SECTION, fill="black", anchor="w")

    # Position bar canvas
    bar_canvas_x = current_width * 0.65
    bar_canvas_y = current_height * 0.55
    box_canvas.create_window(bar_canvas_x, bar_canvas_y, window=bar_canvas)

    # Redraw bars inside the bar_canvas
    create_bar(bar_canvas, [30, 60, 90, 120])


def update_right_canvas(event):
    right_canvas.delete("all")
    current_width = event.width
    current_height = event.height

    # Draw the main rounded rectangle background
    draw_rounded_rect(right_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR)

    # Position titles dynamically
    right_canvas.create_text(20, 20, anchor="nw", text="Recent Transaction", font=FONT_SECTION, fill="black")
    right_canvas.create_text(20, 60, anchor="nw", text="Category", font=FONT_SUBTEXT, fill="black")
    right_canvas.create_text(current_width - 30, 60, anchor="ne", text="Amount", font=FONT_SUBTEXT, fill="black")

    # Position transactions dynamically
    y_offset = 100
    line_height = 28
    for idx, (category, amount) in enumerate(transactions):
        right_canvas.create_text(30, y_offset, anchor="w", text=f"• {category}", font=FONT_TRANSACTION, fill="black")
        right_canvas.create_text(current_width - 30, y_offset, anchor="e", text=f"{amount}", font=FONT_TRANSACTION,
                                 fill="black")
        y_offset += line_height


# Function to draw the custom rounded rectangle on the navbar canvas and place content
def draw_navbar_content(event):
    navbar.delete("all")  # Clear previous drawings
    # Use the new draw_bottom_rounded_rect for the navbar
    draw_bottom_rounded_rect(navbar, 0, 0, event.width, event.height, 20, COLOR_NAVBAR)

    # Place the "TrackU" label on the canvas
    brand_label = tk.Label(navbar, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
    navbar.create_window(20, event.height / 2, window=brand_label, anchor="w")


# --- Main App Window ---
root = tk.Tk()
root.title("TrackU")
root.geometry("950x520")
root.state("zoomed")
root.configure(bg=COLOR_BG)

# --- REVISED ROOT GRID CONFIGURATION ---
# Column 0: Full height sidebar
# Column 1: Top Navbar (fixed height) AND Main Content (takes remaining height)
root.grid_columnconfigure(0, weight=0, minsize=250)  # Fixed width for sidebar
root.grid_columnconfigure(1, weight=1)  # Main content area takes remaining width

# Row 0: Top part (navbar + top part of sidebar)
# Row 1: Bottom part (main content + bottom part of sidebar)
root.grid_rowconfigure(0, weight=0, minsize=65)  # Fixed height for navbar row
root.grid_rowconfigure(1, weight=1)  # Main content row takes remaining height

# --- LEFT SIDEBAR FRAME (Spans both rows in column 0) ---
sidebar_frame = tk.Frame(root, bg=COLOR_SIDEBAR, width=250, highlightthickness=0)  # Sidebar width
sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")  # Placed in row 0, column 0, spans 2 rows
sidebar_frame.grid_propagate(False)  # Prevent children from dictating frame size

# Sidebar layout with grid
sidebar_frame.grid_columnconfigure(0, weight=1)

# Define menu_items before it's used
menu_items = []

# This row will take all remaining space, pushing elements to the top
sidebar_frame.grid_rowconfigure(len(menu_items) * 2, weight=1)  # Adjust index based on how many items + separators

# Sidebar content (excluding brand label, as it's now in the navbar)
row_idx = 0
for item in menu_items:
    if item:
        tk.Label(sidebar_frame, text=item, font=FONT_MENU, bg=COLOR_SIDEBAR, fg="black").grid(row=row_idx, column=0,
                                                                                              pady=10, sticky="ew")
        # Add separator only if not the last item in the list and not an empty string
        if item != "Profile" and item != "":
            tk.Frame(sidebar_frame, bg=COLOR_BOX_BORDER, height=1).grid(row=row_idx + 1, column=0, sticky="ew", padx=10)
            row_idx += 1  # Increment for the separator
    else:  # This handles the empty string for extra spacing
        tk.Label(sidebar_frame, text="", bg=COLOR_SIDEBAR).grid(row=row_idx, column=0, pady=20)
    row_idx += 1  # Increment for the label/empty space

# --- TOP NAVIGATION BAR (Placed in row 0, column 1) ---
navbar = tk.Canvas(root, bg=COLOR_BG, height=65, highlightthickness=0)  # Fixed height for navbar
navbar.grid(row=0, column=1, sticky="nsew")  # Placed in row 0, column 1
navbar.bind("<Configure>", draw_navbar_content)  # Bind drawing to resize

# --- MAIN CONTENT FRAME (Placed in row 1, column 1) ---
main_frame = tk.Frame(root, bg=COLOR_BG)
main_frame.grid(row=1, column=1, sticky="nsew", padx=(45, 0), pady=10)  # Placed in row 1, column 1
main_frame.grid_columnconfigure(0, weight=1, minsize=1)
main_frame.grid_columnconfigure(1, weight=3)
main_frame.grid_rowconfigure(1, weight=1)

tk.Label(main_frame, text="Welcome, [username]", font=FONT_WELCOME, bg=COLOR_BG).grid(
    row=0, column=0, columnspan=2, sticky="w", padx=(0, 0), pady=(0, 10))

# Left Section - Spending Boxes (Total Expenses & Total Savings)
left_frame = tk.Frame(main_frame, bg=COLOR_BG)
left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 0))
left_frame.grid_rowconfigure((0, 1), weight=1)
left_frame.grid_columnconfigure(0, weight=1)

box_titles = ["Total Expenses", "Total Savings"]
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

month_comboboxes = []
bar_canvases = []

for i in range(2):
    box_canvas = tk.Canvas(left_frame, bg=COLOR_BG, highlightthickness=0)
    box_canvas.grid(row=i, column=0, pady=15, sticky="nsew")

    month_combobox = ttk.Combobox(box_canvas, values=months, state="readonly", width=15, font=FONT_SUBTEXT,
                                  justify="center")
    month_combobox.current(0)
    month_comboboxes.append(month_combobox)

    bar_canvas_child = tk.Canvas(box_canvas, width=160, height=180, bg=COLOR_CANVAS_BAR, highlightthickness=0)
    bar_canvases.append(bar_canvas_child)

    box_canvas.bind("<Configure>", lambda event, bc=box_canvas, mc=month_combobox, bt=box_titles[i], at="₱ 0.00",
                                          brc=bar_canvas_child: update_left_box_canvas(event, bc, mc, bt, at, brc))

# Right Section - Recent Transactions
right_canvas = tk.Canvas(main_frame, bg=COLOR_BG, highlightthickness=0)
right_canvas.grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=14)

right_canvas.bind("<Configure>", update_right_canvas)

root.mainloop()