import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os
import subprocess
import sys

# --- Colors ---
COLOR_BG = "#fdfdf5"
COLOR_NAVBAR = "#ffe0b2"  # Top right header color
COLOR_SIDEBAR = "#d6e9d5"  # Sidebar color
COLOR_CANVAS_BAR = "#fdf6e3"  # Background for the recent transactions box (still used for fill)
COLOR_PIE_SLICE_1 = "#4dd0e1"  # Teal
COLOR_PIE_SLICE_2 = "#ff8a65"  # Orange
COLOR_PIE_SLICE_3 = "#ffd54f"  # Red/Yellow

# --- Fonts ---
FONT_BRAND = ("Playfair Display", 20, "bold")
FONT_MENU = ("Playfair Display", 13)
FONT_SECTION = ("Georgia", 16, "bold")
FONT_SUBTEXT = ("Playfair Display", 12)
FONT_TRANSACTION = ("Playfair Display", 11)

LOGO_SIZE_SIDEBAR = (150, 100) # Define size for the sidebar logo (re-added if needed for this view)


# Dummy data for transactions (if still used on this page, otherwise can be removed)
transactions = [
    ("Initial Deposit", "+5000"),
    ("Interest Earned", "+50"),
    ("Savings Goal Transfer", "-200"),
    ("Investment Gain", "+150"),
    ("Emergency Fund Deposit", "+300"),
    ("Automated Savings", "+100"),
    ("Future Purchase Savings", "+75"),
]

# Global image references to prevent garbage collection (for sidebar icons)
sidebar_icon_refs = {}


# --- Helper Function for Sidebar Items ---
def create_sidebar_item(parent_frame, text, icon_name, row_index, command=None):
    item_frame = tk.Frame(parent_frame, bg=COLOR_SIDEBAR)
    item_frame.grid(row=row_index, column=0, sticky="ew", padx=10, pady=5)
    item_frame.grid_columnconfigure(1, weight=1)

    # Construct path relative to the script's directory for icons
    script_dir = os.path.dirname(__file__)
    icon_path = os.path.join(script_dir, "icons", f"{icon_name}.png") # Assumes 'icons' folder is a sibling of this script's folder or within it

    icon_label = None
    try:
        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize((30, 30), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            sidebar_icon_refs[text] = photo # Store reference to prevent garbage collection
            icon_label = tk.Label(item_frame, image=photo, bg=COLOR_SIDEBAR)
        else:
            print(f"Warning: Icon not found at {icon_path}. Using placeholder text.")
            icon_label = tk.Label(item_frame, text="[I]", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR, fg="black")

    except Exception as e:
        print(f"Error loading icon {icon_path}: {e}. Using placeholder text.")
        icon_label = tk.Label(item_frame, text="[I]", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR, fg="black")

    if icon_label:
        icon_label.grid(row=0, column=0, padx=(5, 5), pady=2, sticky="w")

    text_label = tk.Label(item_frame, text=text, font=FONT_MENU, bg=COLOR_SIDEBAR, fg="black")
    text_label.grid(row=0, column=1, sticky="w", padx=(0, 5), pady=2)

    def on_enter(event):
        item_frame.config(bg="#e0e0e0")
        if icon_label: icon_label.config(bg="#e0e0e0")
        text_label.config(bg="#e0e0e0")

    def on_leave(event):
        item_frame.config(bg=COLOR_SIDEBAR)
        if icon_label: icon_label.config(bg=COLOR_SIDEBAR)
        text_label.config(bg=COLOR_SIDEBAR)

    item_frame.bind("<Enter>", on_enter)
    item_frame.bind("<Leave>", on_leave)
    if icon_label:
        icon_label.bind("<Enter>", on_enter)
        icon_label.bind("<Leave>", on_leave)
    text_label.bind("<Enter>", on_enter)
    text_label.bind("<Leave>", on_leave)

    if command:
        item_frame.bind("<Button-1>", lambda e: command())
        if icon_label: icon_label.bind("<Button-1>", lambda e: command())
        text_label.bind("<Button-1>", lambda e: command())

    return item_frame


# --- Drawing Functions ---

def draw_bottom_rounded_rect(canvas, x, y, w, h, r, color):
    """Draws a rectangle with only the bottom corners rounded."""
    canvas.create_rectangle(x, y, x + w, y + r, fill=color, outline=color)
    canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)
    canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x + r, y + h - r, x + w - r, y + h, fill=color, outline=color)


def draw_rounded_rect(canvas, x, y, w, h, r, color, outline_color="", outline_width=0):
    """Draws a rectangle with all four corners rounded, with optional outline."""
    if outline_width > 0 and outline_color:
        canvas.create_arc(x, y, x + 2 * r, y + 2 * r, start=90, extent=90, fill=color, outline=outline_color,
                          width=outline_width)
        canvas.create_arc(x + w - 2 * r, y, x + w, y + 2 * r, start=0, extent=90, fill=color, outline=outline_color,
                          width=outline_width)
        canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=outline_color,
                          width=outline_width)
        canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color,
                          outline=outline_color, width=outline_width)
        canvas.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=outline_color, width=outline_width)
        canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=outline_color, width=outline_width)
    else:  # Draw without outline
        canvas.create_arc(x, y, x + 2 * r, y + 2 * r, start=90, extent=90, fill=color, outline=color)
        canvas.create_arc(x + w - 2 * r, y, x + w, y + 2 * r, start=0, extent=90, fill=color, outline=color)
        canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color)
        canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
        canvas.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color)
        canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)


# --- Functions to draw/update sections on resize ---

# Global labels to be managed by draw_top_right_header_content
tracku_label_tk = None
# Renamed from total_expenses_label_tk to total_savings_label_tk for clarity
total_savings_header_label_tk = None


def draw_top_right_header_content(event):
    """Draws the custom rounded rectangle and places content on the top right header canvas."""
    global tracku_label_tk, total_savings_header_label_tk # Use the correct global variable name
    top_right_header_canvas.delete("all")
    draw_bottom_rounded_rect(top_right_header_canvas, 0, 0, event.width, event.height, 20, COLOR_NAVBAR)

    if tracku_label_tk is None:
        tracku_label_tk = tk.Label(top_right_header_canvas, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
        # Ensure this label is for "Total Savings"
        total_savings_header_label_tk = tk.Label(top_right_header_canvas, text="Total Savings", font=("Georgia", 16),
                                           bg=COLOR_NAVBAR, fg="#222")

    top_right_header_canvas.create_window(30, event.height / 2, window=tracku_label_tk, anchor="w")
    top_right_header_canvas.create_window(event.width - 30, event.height / 2, window=total_savings_header_label_tk,
                                          anchor="e")


# Global reference for the matplotlib canvas widget
canvas_chart_widget_ref = None


def update_pie_chart_section(event, canvas, month_combobox, total_savings_lbl): # Renamed parameter
    """Updates the content of the left-side section (month, pie chart, expenses/savings)."""
    global canvas_chart_widget_ref
    canvas.delete("all")  # Clear the canvas

    current_width = event.width
    current_height = event.height

    # Peso sign watermark for the pie chart section - Draw first, then lower
    canvas.create_text(current_width / 2, current_height / 2, text="₱",
                       font=("Arial", int(current_height * 0.7), "bold"),
                       fill="#f0f0e0", anchor="center", tags="pie_watermark")
    canvas.tag_lower("pie_watermark")  # Ensures it's in the background

    # Position month combobox (centered horizontally at the top)
    canvas.create_window(current_width / 2, 40, window=month_combobox, anchor="n")

    # --- Matplotlib Pie Chart ---
    chart_height_ratio = 0.6
    # Adjusted figsize to be relative to the canvas size in pixels, then converted to inches
    fig, ax = plt.subplots(figsize=(current_width / 100, (current_height * chart_height_ratio) / 100), dpi=100,
                           facecolor=COLOR_BG)
    sizes = [70, 20, 10] # Dummy data for pie slices, representing savings categories perhaps
    colors = [COLOR_PIE_SLICE_1, COLOR_PIE_SLICE_2, COLOR_PIE_SLICE_3]
    explode = (0.02, 0.02, 0.02)

    ax.pie(sizes, colors=colors, explode=explode, startangle=140, wedgeprops=dict(width=0.8, edgecolor=COLOR_BG))
    ax.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_facecolor(COLOR_BG)
    plt.tight_layout(pad=0)

    # Text in the middle of the pie chart
    ax.text(0, 0, 'Savings Breakdown', horizontalalignment='center', verticalalignment='center',
            fontsize=FONT_SECTION[1], color='gray', transform=ax.transAxes)

    if canvas_chart_widget_ref:
        canvas_chart_widget_ref.destroy() # Destroy previous widget to prevent accumulation

    canvas_chart_agg = FigureCanvasTkAgg(fig, master=canvas)
    canvas_chart_widget = canvas_chart_agg.get_tk_widget()
    canvas_chart_widget.config(bg=COLOR_BG) # Ensure widget background matches canvas

    chart_center_y = current_height * (0.15 + chart_height_ratio / 2)
    canvas.create_window(current_width / 2, chart_center_y, window=canvas_chart_widget, anchor="center")
    canvas_chart_widget_ref = canvas_chart_widget # Store reference to the new widget

    # Position the savings label
    total_savings_y = current_height * (0.15 + chart_height_ratio) + 30
    canvas.create_window(current_width / 2, total_savings_y, window=total_savings_lbl, anchor="n") # Use total_savings_lbl

    plt.close(fig) # Close the matplotlib figure to free memory


# Global variables for the category combobox in recent transactions
recent_transaction_category_combobox = None
# recent_transaction_category_combobox_var = None
recent_transaction_category_combobox_window_id = None # To store the canvas window ID for the combobox


def update_recent_transaction_box(event):
    """Updates the content of the right-side recent transactions box on resize."""
    global recent_transaction_category_combobox, recent_transaction_category_combobox_window_id
    recent_transaction_canvas.delete("all") # Clear previous drawings
    current_width = event.width
    current_height = event.height

    # 1. Draw the main rounded rectangle background
    draw_rounded_rect(recent_transaction_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR,
                      outline_width=0)

    # 2. Draw the peso sign watermark. It will be BEHIND anything drawn AFTER it.
    recent_transaction_canvas.create_text(current_width / 2, current_height / 2, text="₱",
                                          font=("Arial", int(current_height * 0.7), "bold"),
                                          fill="#f0f0e0", anchor="center", tags="watermark") # Faded color
    recent_transaction_canvas.tag_lower("watermark") # Ensures it's in the background

    # 3. Draw all other foreground content (headers, combobox, transaction list).
    # These will naturally appear ON TOP of the background and watermark because they are drawn last.

    # Header: "Recent Transaction" and "+" icon
    recent_transaction_canvas.create_text(20, 20, anchor="nw", text="Recent Savings", font=FONT_SECTION, # Changed text
                                          fill="black")
    recent_transaction_canvas.create_text(current_width - 30, 20, anchor="ne", text="+", font=("Arial", 28, "bold"),
                                          fill="black")

    # Column Headers: "Amount" (Category is handled by the dropdown)
    recent_transaction_canvas.create_text(current_width - 30, 60, anchor="ne", text="Amount", font=FONT_SUBTEXT,
                                          fill="black")

    # Category Dropdown - Create/reposition it if its window ID exists
    if recent_transaction_category_combobox is None or not recent_transaction_category_combobox.winfo_exists():
        recent_transaction_category_combobox_var = tk.StringVar(value="Category")
        recent_transaction_category_combobox = ttk.Combobox(
            recent_transaction_canvas,
            textvariable=recent_transaction_category_combobox_var,
            values=["Category", "Deposit", "Transfer", "Interest", "Investment", "Misc."], # Updated values for savings
            state="readonly",
            width=10,
            font=FONT_SUBTEXT,
            justify="center"
        )
        recent_transaction_category_combobox_window_id = recent_transaction_canvas.create_window(
            70, 60, window=recent_transaction_category_combobox, anchor="w"
        )
    else:
        # Update its coordinates and raise it if it already exists
        recent_transaction_canvas.coords(recent_transaction_category_combobox_window_id, 70, 60)
        recent_transaction_canvas.tag_raise(recent_transaction_category_combobox_window_id)


    # Transaction list
    y_offset = 90
    line_height = 28
    for idx, (category, amount) in enumerate(transactions):
        if y_offset + line_height > current_height - 30: # Prevent drawing beyond visible area
            break
        recent_transaction_canvas.create_text(30, y_offset, anchor="w", text=f"• {category}", font=FONT_TRANSACTION,
                                              fill="black")
        recent_transaction_canvas.create_text(current_width - 30, y_offset, anchor="e", text=f"{amount}",
                                              font=FONT_TRANSACTION, fill="black")
        y_offset += line_height



# --- Main App Window ---
def create_total_savings_app():
    root = tk.Tk()
    root.title("TrackU - Total Savings") # Updated title
    root.state("zoomed")
    root.configure(bg=COLOR_BG)

    # --- ROOT GRID CONFIGURATION ---
    root.grid_columnconfigure(0, weight=0, minsize=250)
    root.grid_columnconfigure(1, weight=1)

    root.grid_rowconfigure(0, weight=0, minsize=70)
    root.grid_rowconfigure(1, weight=1)

    # --- LEFT SIDEBAR FRAME (Spans both rows in column 0) ---
    sidebar_frame = tk.Frame(root, bg=COLOR_SIDEBAR, width=250, highlightthickness=0)
    sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
    sidebar_frame.grid_propagate(False)

    sidebar_frame.grid_columnconfigure(0, weight=1)

    # --- Sidebar Logo ---
    # Global variable to keep a reference to the PhotoImage object
    global sidebar_logo_img
    sidebar_logo_img = None
    try:
        # Assuming 'testlogo.png' is in the same directory as this script, or in 'icons' folder
        script_dir = os.path.dirname(__file__)
        logo_path_attempt = os.path.join(script_dir, "testlogo.png")
        if not os.path.exists(logo_path_attempt):
            logo_path_attempt = os.path.join(script_dir, "icons", "testlogo.png") # Try in 'icons' folder too

        if os.path.exists(logo_path_attempt):
            img = Image.open(logo_path_attempt).resize(LOGO_SIZE_SIDEBAR, Image.LANCZOS)
            sidebar_logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(sidebar_frame, image=sidebar_logo_img, bg=COLOR_SIDEBAR, borderwidth=0)
            logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
        else:
            logo_label = tk.Label(sidebar_frame, text="TrackU Logo", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR, fg="darkgray")
            logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
            print("Warning: testlogo.png not found for sidebar. Using placeholder text.")
    except Exception as e:
        print(f"Error loading sidebar logo: {e}. Using placeholder text.")
        logo_label = tk.Label(sidebar_frame, text="TrackU Logo", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR, fg="darkgray")
        logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")


    sidebar_items_data = [
        ("Dashboard", "dashboard"),
        ("Total Savings", "savings"),
        ("Total Expenses", "expenses"),
        ("Profile", "profile")
    ]

    row_idx = 1 # Start creating sidebar items from row 1, after the logo (row 0)
    for text, icon_name in sidebar_items_data:
        create_sidebar_item(sidebar_frame, text, icon_name, row_idx)
        row_idx += 1

    sidebar_frame.grid_rowconfigure(row_idx, weight=1) # Push sidebar items to the top

    # --- TOP RIGHT HEADER / NAVBAR (Canvas for drawing rounded bottom corners) ---
    global top_right_header_canvas
    top_right_header_canvas = tk.Canvas(root, bg=COLOR_BG, height=70, highlightthickness=0)
    top_right_header_canvas.grid(row=0, column=1, sticky="nsew")
    top_right_header_canvas.bind("<Configure>", draw_top_right_header_content)

    # --- MAIN CONTENT FRAME (Placed in row 1, column 1, below the top right header) ---
    main_content_area = tk.Frame(root, bg=COLOR_BG)
    main_content_area.grid(row=1, column=1, sticky="nsew", padx=30, pady=20)
    main_content_area.grid_columnconfigure(0, weight=1, minsize=300)
    main_content_area.grid_columnconfigure(1, weight=1)
    main_content_area.grid_rowconfigure(0, weight=1)

    # --- LEFT SECTION: Pie Chart and Savings Details ---
    pie_chart_section_canvas = tk.Canvas(main_content_area, bg=COLOR_BG, highlightthickness=0)
    pie_chart_section_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=10)

    # --- MONTHS DROPDOWN (for Pie Chart Section) ---
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    month_var = tk.StringVar(value="January")
    month_combo = ttk.Combobox(pie_chart_section_canvas, textvariable=month_var, values=months,
                               state="readonly", font=FONT_SUBTEXT, justify="center", width=10)
    month_combo.current(0)


    total_savings_amount_lbl = tk.Label(pie_chart_section_canvas, text="Total Savings:\n₱ 100,000.00", # Changed text here
                                         font=("Georgia", 13), bg=COLOR_BG, fg="black", justify=tk.LEFT)

    pie_chart_section_canvas.bind("<Configure>",
                                  lambda event: update_pie_chart_section(event, pie_chart_section_canvas, month_combo,
                                                                         total_savings_amount_lbl)) # Passed correct label

    # --- RIGHT SECTION: Recent Transactions (now Recent Savings) ---
    global recent_transaction_canvas # Declare as global to be accessible in update function
    recent_transaction_canvas = tk.Canvas(main_content_area, bg=COLOR_BG, highlightthickness=0)
    recent_transaction_canvas.grid(row=0, column=1, sticky="nsew", pady=10)

    # Initialize the combobox for recent transactions here if it's not global
    # It's already global, so ensure it's initialized once outside the update function.
    # The global recent_transaction_category_combobox_var and recent_transaction_category_combobox
    # are defined before the update_recent_transaction_box function, which is good.
    # However, the window ID is also global and needs to be handled carefully.

    recent_transaction_canvas.bind("<Configure>", update_recent_transaction_box)

    root.mainloop()


if __name__ == "__main__":
    create_total_savings_app()
