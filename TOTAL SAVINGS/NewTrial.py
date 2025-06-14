import tkinter as tk
from tkinter import ttk, font
# Re-import matplotlib as it's used in the pie chart section
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# --- Colors ---
COLOR_BG = "#fdfdf5"
COLOR_NAVBAR = "#ffe0b2"  # Navbar color (now only for the right side top bar)
COLOR_SIDEBAR = "#d6e9d5"  # Sidebar color
COLOR_LINE = "#d3d3d3"
COLOR_CANVAS_BAR = "#fdf6e3"
COLOR_BOX_BORDER = "black"
COLOR_TRANSACTION_PESO = "#f0e68c"

# --- Fonts ---
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
NAVBAR_RADIUS = 20  # Radius for navbar rounded corners (now applies to right-top bar)

# --- Sample Data ---
categories_data = ["Food", "School Supplies", "Emergency Funds", "School Fees", "General Savings", "Personal Goal",
                   "Future Purchases"]
amounts_data = [100, 100, 100, 100, 100, 100, 100]

transactions_list = [
    ("Food", "-100"),
    ("Schoo Suplies", "-100"),
    ("Emergency Funds", "-100"),
    ("School Fees", "-100"),
    ("Food", "-100"),
    ("General Savings", "-100"),
    ("Personal Goal", "-100"),
    ("Future Purchases", "-100"),
]


# --- Helper Functions ---

# Function to draw a rectangle with only bottom corners rounded
def draw_bottom_rounded_rect(canvas, x, y, w, h, r, color):
    # This function is designed to round the bottom corners of a full-width rect.
    # We will adjust its usage for the new navbar position.
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


def update_right_canvas(event):
    if 'transactions_bg_canvas' in globals():
        transactions_bg_canvas.delete("all")
        current_width = event.width
        current_height = event.height
        draw_rounded_rect(transactions_bg_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR)

        transactions_bg_canvas.create_text(
            current_width / 2, current_height / 2,
            text="₱",
            font=("Arial", 250, "bold"),
            fill=COLOR_TRANSACTION_PESO,
            justify="center",
            tags="peso_watermark"
        )


def draw_navbar_content(event):
    navbar.delete("all")
    # Navbar now only occupies the right column. It still needs its bottom-right corner rounded.
    # The left edge will meet the sidebar, so it won't be rounded on the left.
    # We'll draw a rectangle and then a bottom-right arc.
    current_width = event.width
    current_height = event.height
    radius = NAVBAR_RADIUS

    # Draw the main rectangular part of the navbar
    navbar.create_rectangle(0, 0, current_width, current_height, fill=COLOR_NAVBAR, outline=COLOR_NAVBAR)

    # Draw the bottom-right arc
    navbar.create_arc(current_width - 2 * radius, current_height - 2 * radius, current_width, current_height,
                      start=270, extent=90, fill=COLOR_NAVBAR, outline=COLOR_NAVBAR)
    navbar.create_rectangle(current_width - radius, current_height - radius, current_width, current_height,
                            fill=COLOR_NAVBAR, outline=COLOR_NAVBAR)


    # Place the "TrackU" label (now likely in sidebar)
    # The brand label "TrackU" should logically be in the sidebar if the sidebar extends to the top.
    # However, if you want "TrackU" to remain in the navbar (but only on the right side), we can place it here.
    # For now, keeping it in the navbar as per previous versions, but be aware of visual implications.
    # Let's move "TrackU" label to the sidebar, and only "Total Savings" remains in the navbar.
    # If "TrackU" is to be on the navbar still, it should be placed with respect to its new, smaller width.
    # brand_label = tk.Label(navbar, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
    # navbar.create_window(30, event.height / 2, window=brand_label, anchor="w")

    # Place "Total Savings" on the right side of the navbar
    total_savings_label = tk.Label(navbar, text="Total Savings", font=FONT_SECTION, bg=COLOR_NAVBAR, fg="black")
    # Adjust position for the smaller navbar (starts at x=0 for this canvas)
    navbar.create_window(current_width - 30, current_height / 2, window=total_savings_label, anchor="e")


# --- Main App Window ---
root = tk.Tk()
root.title("TrackU")
root.geometry("950x520")
root.state("zoomed")
root.configure(bg=COLOR_BG)

# --- Root Grid Configuration ---
# Row 0: Top section (top of sidebar + navbar)
# Row 1: Bottom section (rest of sidebar + main content)
root.grid_rowconfigure(0, weight=0, minsize=65)  # Fixed height for top bar area
root.grid_rowconfigure(1, weight=1)  # Remaining height for content

# Columns: Sidebar (fixed) and Main Content Area (flexible)
root.grid_columnconfigure(0, weight=0, minsize=350)  # Sidebar fixed width
root.grid_columnconfigure(1, weight=1)  # Main content area takes remaining width

# --- LEFT SIDEBAR FRAME (Spans both rows in column 0) ---
sidebar_frame = tk.Frame(root, bg=COLOR_SIDEBAR, width=350, highlightthickness=0)
sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew") # <<< HIGHLIGHT: Sidebar now spans row 0 and 1
sidebar_frame.grid_propagate(False)

# Add "TrackU" brand label to the top of the sidebar
brand_label_sidebar = tk.Label(sidebar_frame, text="TrackU", font=FONT_BRAND, bg=COLOR_SIDEBAR, fg="black")
brand_label_sidebar.grid(row=0, column=0, sticky="nw", padx=30, pady=20) # Positioned at the top-left of sidebar

# Sidebar content layout (using internal grid)
sidebar_frame.grid_columnconfigure(0, weight=1)

menu_items_placeholders = [
    "Dashboard",
    "Total Savings",
    "Total Expenses",
    "Profile"
]

# This row will take all remaining space, pushing elements below brand_label_sidebar
# Start menu items from row 1, as row 0 is for the brand label
sidebar_frame.grid_rowconfigure(len(menu_items_placeholders) + 1, weight=1) # +1 because brand_label is in row 0

row_idx = 1 # Start menu items from row 1
for _ in menu_items_placeholders:
    item_frame = tk.Frame(sidebar_frame, bg=COLOR_SIDEBAR, height=50)
    item_frame.grid(row=row_idx, column=0, pady=10, sticky="ew")
    row_idx += 1


# --- TOP NAVIGATION BAR (Now only in column 1, row 0) ---
navbar = tk.Canvas(root, bg=COLOR_BG, height=65, highlightthickness=0)
navbar.grid(row=0, column=1, sticky="nsew") # <<< HIGHLIGHT: Navbar is now only in column 1, row 0
navbar.bind("<Configure>", draw_navbar_content)


# --- MAIN CONTENT FRAME (Placed in row 1, column 1) ---
right_panel_frame = tk.Frame(root, bg=COLOR_BG)
right_panel_frame.grid(row=1, column=1, sticky="nsew", padx=(45, 10), pady=10)
right_panel_frame.grid_rowconfigure(0, weight=1)
right_panel_frame.grid_columnconfigure(0, weight=1)

main_frame = tk.Frame(right_panel_frame, bg=COLOR_BG)
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.grid_columnconfigure(0, weight=1, minsize=1)
main_frame.grid_columnconfigure(1, weight=3)
main_frame.grid_rowconfigure(0, weight=0)
main_frame.grid_rowconfigure(1, weight=1)

tk.Label(main_frame, text="Welcome, [username]", font=FONT_WELCOME, bg=COLOR_BG).grid(
    row=0, column=0, columnspan=2, sticky="w", padx=(0, 0), pady=(0, 10))

# --- Left Section: Pie Chart and Savings Details ---
left_content_frame = tk.Frame(main_frame, bg=COLOR_BG)
left_content_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=0)
left_content_frame.grid_rowconfigure(0, weight=0)
left_content_frame.grid_rowconfigure(1, weight=1)
left_content_frame.grid_rowconfigure(2, weight=0)
left_content_frame.grid_columnconfigure(0, weight=1)

pie_chart_bg_canvas = tk.Canvas(left_content_frame, bg=COLOR_BG, highlightthickness=0)
pie_chart_bg_canvas.grid(row=0, column=0, rowspan=3, sticky="nsew")
pie_chart_bg_canvas.grid_propagate(False)

def update_pie_chart_canvas_bg(event):
    pie_chart_bg_canvas.delete("bg_rect")
    draw_rounded_rect(pie_chart_bg_canvas, 0, 0, event.width, event.height, 20, COLOR_CANVAS_BAR)
pie_chart_bg_canvas.bind("<Configure>", update_pie_chart_canvas_bg)

month_dropdown = ttk.Combobox(pie_chart_bg_canvas, values=["Month", "January", "February", "March"],
                              font=FONT_SUBTEXT, justify="center")
month_dropdown.current(0)
pie_chart_bg_canvas.create_window(pie_chart_bg_canvas.winfo_width() / 2, 40, window=month_dropdown, anchor="center",
                                  tags="month_dropdown_window")

fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
colors_for_pie = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#c4e17f']
ax.pie(amounts_data, labels=categories_data, colors=colors_for_pie, startangle=90,
       wedgeprops={'edgecolor': 'white', 'linewidth': 1})
ax.axis('equal')

chart_canvas = FigureCanvasTkAgg(fig, master=pie_chart_bg_canvas)
chart_canvas_widget = chart_canvas.get_tk_widget()
pie_chart_bg_canvas.create_window(pie_chart_bg_canvas.winfo_width() / 2, pie_chart_bg_canvas.winfo_height() / 2 - 20,
                                  window=chart_canvas_widget, anchor="center",
                                  tags="chart_window")

total_savings_amount_label = tk.Label(pie_chart_bg_canvas, text="Total Savings:\n+ ₱ 100,000.00", font=FONT_SECTION,
                                      bg=COLOR_CANVAS_BAR, fg="black")
pie_chart_bg_canvas.create_window(pie_chart_bg_canvas.winfo_width() / 2, pie_chart_bg_canvas.winfo_height() - 50,
                                  window=total_savings_amount_label, anchor="s",
                                  tags="total_savings_label_window")

def reposition_pie_chart_elements(event):
    update_pie_chart_canvas_bg(event)
    pie_chart_bg_canvas.coords("month_dropdown_window", event.width / 2, 40)
    pie_chart_bg_canvas.coords("chart_window", event.width / 2, event.height / 2 - 20)
    pie_chart_bg_canvas.coords("total_savings_label_window", event.width / 2, event.height - 50)
pie_chart_bg_canvas.bind("<Configure>", reposition_pie_chart_elements)

# --- Right Section: Recent Transactions ---
transactions_bg_canvas = tk.Canvas(main_frame, bg=COLOR_BG, highlightthickness=0)
transactions_bg_canvas.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=0)
transactions_bg_canvas.grid_propagate(False)

right_content_widgets_frame = tk.Frame(transactions_bg_canvas, bg=COLOR_CANVAS_BAR)
right_content_widgets_frame.pack(fill="both", expand=True, padx=20, pady=20)
right_content_widgets_frame.grid_rowconfigure(0, weight=0)
right_content_widgets_frame.grid_rowconfigure(1, weight=0)
right_content_widgets_frame.grid_rowconfigure(2, weight=1)
right_content_widgets_frame.grid_rowconfigure(3, weight=0)
right_content_widgets_frame.grid_columnconfigure(0, weight=1)

transactions_bg_canvas.bind("<Configure>", update_right_canvas)

tk.Label(right_content_widgets_frame, text="Recent Transaction", font=FONT_SECTION, bg=COLOR_CANVAS_BAR,
         fg="black").grid(row=0, column=0, pady=(0, 10), sticky="w")

category_filter = ttk.Combobox(right_content_widgets_frame, values=["Category"] + categories_data,
                               font=FONT_SUBTEXT, justify="center")
category_filter.current(0)
category_filter.grid(row=1, column=0, pady=(0, 10), sticky="ew")

transactions_scroll_frame = tk.Frame(right_content_widgets_frame, bg=COLOR_CANVAS_BAR)
transactions_scroll_frame.grid(row=2, column=0, sticky="nsew")
transactions_inner_canvas = tk.Canvas(transactions_scroll_frame, bg=COLOR_CANVAS_BAR, highlightthickness=0)
transactions_inner_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
transactions_scrollbar = ttk.Scrollbar(transactions_scroll_frame, orient="vertical",
                                       command=transactions_inner_canvas.yview)
transactions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
transactions_inner_canvas.configure(yscrollcommand=transactions_scrollbar.set)
transactions_inner_canvas.bind('<Configure>', lambda e: transactions_inner_canvas.configure(
    scrollregion=transactions_inner_canvas.bbox("all")))
transactions_content_frame = tk.Frame(transactions_inner_canvas, bg=COLOR_CANVAS_BAR)
transactions_inner_canvas.create_window((0, 0), window=transactions_content_frame, anchor="nw")
for cat, amt in transactions_list:
    tk.Label(transactions_content_frame, text=f"• {cat:<20} {amt}", font=FONT_TRANSACTION, bg=COLOR_CANVAS_BAR,
             fg="black").pack(anchor='w', padx=5, pady=2)

tk.Button(right_content_widgets_frame, text="+", font=FONT_BUTTON, bg='black', fg='white', width=2,
          bd=0, activebackground="gray").grid(row=3, column=0, pady=10)

root.mainloop()