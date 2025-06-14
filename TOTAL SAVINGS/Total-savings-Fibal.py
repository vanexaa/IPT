import tkinter as tk
from tkinter import ttk, font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# --- Colors (from previous code) ---
COLOR_BG = "#fdfdf5"
COLOR_NAVBAR = "#ffe0b2"
COLOR_SIDEBAR = "#d6e9d5"
COLOR_LINE = "#d3d3d3"
COLOR_CANVAS_BAR = "#fdf6e3" # Used for rounded boxes like transactions list
COLOR_BOX_BORDER = "black"

# --- Fonts (from previous code) ---
FONT_BRAND = ("Playfair Display", 20, "bold")
FONT_MENU = ("Playfair Display", 13)
FONT_SECTION = ("Georgia", 16, "bold") # Used for "Recent Transaction" title
FONT_SUBTEXT = ("Playfair Display", 12) # Used for "Category" / "Amount" headers
FONT_AMOUNT = ("Georgia", 24, "underline") # Not directly used for currency, but keeping
FONT_TRANSACTION = ("Playfair Display", 11) # Used for transaction list items
FONT_BUTTON = ("Arial", 25) # For the old menu button, repurposed for '+'
FONT_WELCOME = ("Playfair Display", 22, "bold") # For "Welcome, [username]"

# --- Chart Colors (from new code, but kept specific) ---
BAR_COLOR = "#fdf6e3" # Not directly used for pie chart
BAR_FILL_COLOR = "#ffa726" # Not directly used for pie chart

# Sample Data (from new code)
categories_data = ["Food", "School Supplies", "Emergency Funds", "School Fees", "General Savings", "Personal Goal", "Future Purchases"]
amounts_data = [100, 100, 100, 100, 100, 100, 100] # Dummy data for pie chart

transactions_list = [
    ("Food", "-100"),
    ("School Supplies", "-100"),
    ("Emergency Funds", "-100"),
    ("School Fees", "-100"),
    ("Food", "-100"),
    ("General Savings", "-100"),
    ("Personal Goal", "-100"),
    ("Future Purchases", "-100"),
]

# --- Helper Functions (from previous code, adapted) ---

# Function to draw a rectangle with only bottom corners rounded
def draw_bottom_rounded_rect(canvas, x, y, w, h, r, color):
    canvas.create_rectangle(x, y, x + w, y + r, fill=color, outline=color)
    canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)
    canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x + r, y + h - r, x + w - r, y + h, fill=color, outline=color)

# Function to draw rounded rectangle (for general use where all 4 corners are rounded)
def draw_rounded_rect(canvas, x, y, w, h, r, color):
    canvas.create_arc(x, y, x + 2 * r, y + 2 * r, start=90, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y, x + w, y + 2 * r, start=0, extent=90, fill=color, outline=color)
    canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color)
    canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)

# Function to draw the custom rounded rectangle on the navbar canvas and place content
def draw_navbar_content(event):
    navbar.delete("all")
    # Increased radius for more pronounced rounding
    NAVBAR_RADIUS = 25
    draw_bottom_rounded_rect(navbar, 0, 0, event.width, event.height, NAVBAR_RADIUS, COLOR_NAVBAR)
    brand_label = tk.Label(navbar, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
    # Centered the brand label horizontally
    navbar.create_window(event.width / 2, event.height / 2, window=brand_label, anchor="center")

# Function to update the right content canvas (recent transactions) on resize
def update_right_canvas(event):
    transactions_bg_canvas.delete("all")
    current_width = event.width
    current_height = event.height

    draw_rounded_rect(transactions_bg_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR)


# --- Main App Window ---
root = tk.Tk()
root.title("TrackU")
root.geometry("950x520")
root.state("zoomed")
root.configure(bg=COLOR_BG)

# --- Root Grid Configuration (Sidebar full height, Navbar next to it) ---
# Row 0: Only one row for the whole window height
root.grid_rowconfigure(0, weight=1)
# Column 0: Fixed width for the sidebar
root.grid_columnconfigure(0, weight=0, minsize=250)
# Column 1: Remaining space for the right panel (navbar + main content)
root.grid_columnconfigure(1, weight=1)


# --- Left Sidebar Frame (Spans full height of the root window) ---
sidebar_frame = tk.Frame(root, bg=COLOR_SIDEBAR, highlightthickness=0)
sidebar_frame.grid(row=0, column=0, sticky="nsew") # Placed in column 0, spans full height
sidebar_frame.grid_propagate(False) # Prevent children from dictating frame size

# Sidebar content layout (using internal grid)
sidebar_frame.grid_columnconfigure(0, weight=1)
menu_items = ["Dashboard", "Total Expenses", "Total Savings", "", "Profile"]
# This row will take all remaining space, pushing elements to the top
sidebar_frame.grid_rowconfigure(len(menu_items) * 2, weight=1) # Adjust index for spacing

row_idx = 0
for item in menu_items:
    if item:
        tk.Label(sidebar_frame, text=item, font=FONT_MENU, bg=COLOR_SIDEBAR, fg="black").grid(row=row_idx, column=0, pady=10, sticky="ew")
        if item != "Profile":
            tk.Frame(sidebar_frame, bg=COLOR_BOX_BORDER, height=1).grid(row=row_idx + 1, column=0, sticky="ew", padx=10)
            row_idx += 1 # Increment for the separator
    else: # Handles the empty string for extra spacing
        tk.Label(sidebar_frame, text="", bg=COLOR_SIDEBAR).grid(row=row_idx, column=0, pady=20)
    row_idx += 1 # Increment for the label/empty space


# --- Right Panel Frame (Holds Navbar and Main Content Area) ---
right_panel_frame = tk.Frame(root, bg=COLOR_BG)
right_panel_frame.grid(row=0, column=1, sticky="nsew") # Placed in root's column 1, takes full height

# Configure internal grid for right_panel_frame:
# Row 0: Navbar (fixed height)
# Row 1: Main content area (takes remaining height)
right_panel_frame.grid_rowconfigure(0, weight=0, minsize=65) # Fixed height for navbar
right_panel_frame.grid_rowconfigure(1, weight=1) # Main content takes remaining height
right_panel_frame.grid_columnconfigure(0, weight=1) # Only one column in this internal grid


# --- Top Navigation Bar (inside right_panel_frame) ---
navbar = tk.Canvas(right_panel_frame, bg=COLOR_NAVBAR, height=65, highlightthickness=0)
navbar.grid(row=0, column=0, sticky="nsew") # Placed in right_panel_frame, row 0, column 0
navbar.bind("<Configure>", draw_navbar_content) # Bind drawing to resize


# --- Main Content Frame (inside right_panel_frame) ---
main_frame = tk.Frame(right_panel_frame, bg=COLOR_BG)
main_frame.grid(row=1, column=0, sticky="nsew", padx=(45, 10), pady=10) # Added right padding

# Welcome Text
tk.Label(main_frame, text="Welcome, [username]", font=FONT_WELCOME, bg=COLOR_BG, fg="black").grid(
    row=0, column=0, columnspan=2, sticky="w", padx=(0, 0), pady=(0, 10))


# --- Left Section: Pie Chart and Savings Details ---
left_content_frame = tk.Frame(main_frame, bg=COLOR_BG)
left_content_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=0) # Add padding between left and right sections
left_content_frame.grid_rowconfigure(0, weight=0) # for combobox
left_content_frame.grid_rowconfigure(1, weight=1) # for pie chart
left_content_frame.grid_rowconfigure(2, weight=0) # for total savings label
left_content_frame.grid_columnconfigure(0, weight=1)


# Month Dropdown
month_dropdown = ttk.Combobox(left_content_frame, values=["Month", "January", "February", "March"],
                              font=FONT_SUBTEXT, justify="center")
month_dropdown.current(0)
month_dropdown.grid(row=0, column=0, pady=10, sticky="ew")


# Matplotlib Pie Chart
fig, ax = plt.subplots(figsize=(4, 4), dpi=100) # figsize adjusted, dpi for clarity
colors_for_pie = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6','#c4e17f'] # Softer palette
ax.pie(amounts_data, labels=categories_data, colors=colors_for_pie, startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 1})
ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.

chart_canvas = FigureCanvasTkAgg(fig, master=left_content_frame)
chart_canvas_widget = chart_canvas.get_tk_widget()
chart_canvas_widget.grid(row=1, column=0, sticky="nsew")


# Total Savings Label
tk.Label(left_content_frame, text="Total Savings:\n₱ 100,000.00", font=FONT_SECTION, bg=COLOR_BG, fg="black").grid(row=2, column=0, pady=10)


# --- Right Section: Recent Transactions (Revised) ---
# This frame will hold all content of the right panel, including the "rounded" effect.
# The rounded effect will be applied by drawing on a canvas that is placed beneath these widgets,
# or by using a custom widget that handles its own background.
# Given previous code, let's use a canvas behind it for the rounded background, and place widgets on top.

# Create a canvas for the rounded background of the right transactions section
transactions_bg_canvas = tk.Canvas(main_frame, bg=COLOR_BG, highlightthickness=0)
transactions_bg_canvas.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=0)
transactions_bg_canvas.grid_propagate(False) # Prevent it from resizing based on children

# Create a frame to hold the actual widgets for recent transactions.
# This frame will be placed on top of the transactions_bg_canvas.
right_content_widgets_frame = tk.Frame(transactions_bg_canvas, bg=COLOR_CANVAS_BAR)
right_content_widgets_frame.pack(fill="both", expand=True, padx=20, pady=20) # Padding inside the rounded box

# Layout for widgets inside right_content_widgets_frame
right_content_widgets_frame.grid_rowconfigure(0, weight=0) # Title
right_content_widgets_frame.grid_rowconfigure(1, weight=0) # Category filter
right_content_widgets_frame.grid_rowconfigure(2, weight=1) # Transactions list (scrollable)
right_content_widgets_frame.grid_rowconfigure(3, weight=0) # Plus button
right_content_widgets_frame.grid_columnconfigure(0, weight=1)


# Function to draw the rounded background for the transactions area
# This function is bound to the transactions_bg_canvas's <Configure> event
transactions_bg_canvas.bind("<Configure>", update_right_canvas)


# Recent Transaction Title
tk.Label(right_content_widgets_frame, text="Recent Transaction", font=FONT_SECTION, bg=COLOR_CANVAS_BAR, fg="black").grid(row=0, column=0, pady=(0, 10), sticky="w")


# Category Filter
category_filter = ttk.Combobox(right_content_widgets_frame, values=["Category"] + categories_data,
                               font=FONT_SUBTEXT, justify="center")
category_filter.current(0)
category_filter.grid(row=1, column=0, pady=(0, 10), sticky="ew") # Use sticky="ew" to make it wide


# Frame for Scrollable Transactions
transactions_scroll_frame = tk.Frame(right_content_widgets_frame, bg=COLOR_CANVAS_BAR)
transactions_scroll_frame.grid(row=2, column=0, sticky="nsew")

# Use a Canvas inside this frame to draw the transaction text, allowing for a scrollbar
transactions_inner_canvas = tk.Canvas(transactions_scroll_frame, bg=COLOR_CANVAS_BAR, highlightthickness=0)
transactions_inner_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

transactions_scrollbar = ttk.Scrollbar(transactions_scroll_frame, orient="vertical", command=transactions_inner_canvas.yview)
transactions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

transactions_inner_canvas.configure(yscrollcommand=transactions_scrollbar.set)
transactions_inner_canvas.bind('<Configure>', lambda e: transactions_inner_canvas.configure(scrollregion = transactions_inner_canvas.bbox("all")))

# Create another frame inside the canvas to hold the labels
transactions_content_frame = tk.Frame(transactions_inner_canvas, bg=COLOR_CANVAS_BAR)
transactions_inner_canvas.create_window((0, 0), window=transactions_content_frame, anchor="nw")

# Populate transaction labels within transactions_content_frame
for cat, amt in transactions_list:
   tk.Label(transactions_content_frame, text=f"• {cat:<20} {amt}", font=FONT_TRANSACTION, bg=COLOR_CANVAS_BAR, fg="black").pack(anchor='w', padx=5, pady=2)


# Add Button
tk.Button(right_content_widgets_frame, text="+", font=FONT_BUTTON, bg='black', fg='white', width=2,
          bd=0, activebackground="gray").grid(row=3, column=0, pady=10) # Using FONT_BUTTON for size


root.mainloop()