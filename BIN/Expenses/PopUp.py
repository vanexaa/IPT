import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import pyglet
import os
import subprocess
import sys

# Attempt to load custom font
try:
    # This path might need adjustment based on where 'Playfair Display.ttf' is located relative to the script
    # For now, assuming it's in the same directory or a system-accessible font location
    pyglet.font.add_file('Playfair Display.ttf')
except Exception as e:
    print(f"Warning: Could not load Playfair Display.ttf. Using default system fonts. Error: {e}")

# --- Colors ---
COLOR_BG = "#fdfdf5"
COLOR_NAVBAR = "#ffe0b2"  # Top right header color
COLOR_SIDEBAR = "#d6e9d5"  # Sidebar color
COLOR_CANVAS_BAR = "#fdf6e3"  # Background for the recent transactions box (still used for fill)
COLOR_PIE_SLICE_1 = "#4dd0e1"  # Teal for Savings
COLOR_PIE_SLICE_2 = "#ff8a65"  # Orange for Savings
COLOR_PIE_SLICE_3 = "#ffd54f"  # Yellow for Savings
COLOR_BOX_BORDER = "black"

# --- Fonts ---
FONT_BRAND = ("Playfair Display", 20, "bold")
FONT_MENU = ("Playfair Display", 13)
FONT_SECTION = ("Georgia", 16, "bold")
FONT_SUBTEXT = ("Playfair Display", 12)
FONT_TRANSACTION = ("Playfair Display", 11)

LOGO_SIZE_SIDEBAR = (150, 100)

# Dummy data for transactions, now representing savings activities
transactions = [
    ("Initial Deposit", "+5000"),
    ("Interest Earned", "+50"),
    ("Savings Goal Transfer", "-200"),  # Negative indicates money moving out of general savings
    ("Investment Gain", "+150"),
    ("Emergency Fund Deposit", "+300"),
    ("Automated Savings", "+100"),
    ("Future Purchase Savings", "+75"),
]

# Global image references to prevent garbage collection (for sidebar icons)
sidebar_icon_refs = {}


def on_menu_item_click(item_name, current_root):
    """Handles the click event for sidebar menu items."""
    script_dir = os.path.dirname(__file__)
    script_to_launch = None
    if item_name == "Dashboard":
        script_to_launch = os.path.join(script_dir, "..", "DASHBOARD", "dashboard.py")
    elif item_name == "Total Expenses":
        # Assumes expenses.py is in the same directory as this savings.py
        script_to_launch = os.path.join(script_dir, "expenses.py")
    elif item_name == "Total Savings":
        # This is the current file, so we do nothing or could refresh if needed
        print("Already on Total Savings page!")
        return
    elif item_name == "Profile":
        # Placeholder for Profile action
        print("Profile clicked!")
        return

    if script_to_launch:
        try:
            # Launch the script in a new process
            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NEW_CONSOLE

            subprocess.Popen(
                [sys.executable, script_to_launch],
                creationflags=creationflags
            )
        except Exception as e:
            print(f"Failed to launch {script_to_launch}: {e}")
        finally:
            current_root.destroy()  # Close the current window


# --- Helper Function for Sidebar Items ---
def create_sidebar_item(parent_frame, text, icon_name, row_index, command_func, current_page_name="Total Savings"):
    item_frame = tk.Frame(parent_frame, bg=COLOR_SIDEBAR)
    item_frame.grid(row=row_index, column=0, sticky="ew", padx=10, pady=5)
    # Removed: item_frame.grid_columnconfigure(1, weight=1) as there are no icons

    # Highlight if it's the current page
    if text == current_page_name:
        item_frame.config(bg=COLOR_NAVBAR)  # Use navbar color to indicate active

    # Removed all icon-related code here. Only the text label remains.
    text_label = tk.Label(item_frame, text=text, font=FONT_MENU, bg=item_frame.cget("bg"), fg="black")
    text_label.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=2) # Changed column to 0

    def on_enter(event):
        if text != current_page_name:  # Only change color if not the current page
            item_frame.config(bg="#e0e0e0")
            text_label.config(bg="#e0e0e0")

    def on_leave(event):
        if text != current_page_name:  # Revert only if not the current page
            item_frame.config(bg=COLOR_SIDEBAR)
            text_label.config(bg=COLOR_SIDEBAR)

    item_frame.bind("<Enter>", on_enter)
    item_frame.bind("<Leave>", on_leave)
    text_label.bind("<Enter>", on_enter)
    text_label.bind("<Leave>", on_leave)

    # Bind command to all relevant parts
    item_frame.bind("<Button-1>", lambda e: command_func(text))
    text_label.bind("<Button-1>", lambda e: command_func(text))

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
total_savings_header_label_tk = None


def draw_top_right_header_content(event):
    """Draws the custom rounded rectangle and places content on the top right header canvas."""
    global tracku_label_tk, total_savings_header_label_tk
    top_right_header_canvas.delete("all")
    draw_bottom_rounded_rect(top_right_header_canvas, 0, 0, event.width, event.height, 20, COLOR_NAVBAR)

    if tracku_label_tk is None:
        tracku_label_tk = tk.Label(top_right_header_canvas, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
        total_savings_header_label_tk = tk.Label(top_right_header_canvas, text="Total Savings", font=("Georgia", 16),
                                                 bg=COLOR_NAVBAR, fg="#222")

    top_right_header_canvas.create_window(30, event.height / 2, window=tracku_label_tk, anchor="w")
    top_right_header_canvas.create_window(event.width - 30, event.height / 2, window=total_savings_header_label_tk,
                                          anchor="e")


# Global reference for the matplotlib canvas widget
canvas_chart_widget_ref = None


def update_pie_chart_section(event, canvas, month_combobox, total_savings_lbl):
    """Updates the content of the left-side section (month, pie chart, savings details)."""
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
    sizes = [70, 20,
             10]  # Dummy data for pie slices, representing savings categories perhaps (e.g., Main Savings, Emergency, Investments)
    colors = [COLOR_PIE_SLICE_1, COLOR_PIE_SLICE_2, COLOR_PIE_SLICE_3]
    explode = (0.02, 0.02, 0.02)

    ax.pie(sizes, colors=colors, explode=explode, startangle=140, wedgeprops=dict(width=0.8, edgecolor=COLOR_BG))
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_facecolor(COLOR_BG)
    plt.tight_layout(pad=0)

    # Text in the middle of the pie chart
    ax.text(0, 0, 'Savings Breakdown', horizontalalignment='center', verticalalignment='center',
            fontsize=FONT_SECTION[1], color='gray', transform=ax.transAxes)

    if canvas_chart_widget_ref:
        canvas_chart_widget_ref.destroy()  # Destroy previous widget to prevent accumulation

    canvas_chart_agg = FigureCanvasTkAgg(fig, master=canvas)
    canvas_chart_widget = canvas_chart_agg.get_tk_widget()
    canvas_chart_widget.config(bg=COLOR_BG)  # Ensure widget background matches canvas

    chart_center_y = current_height * (0.15 + chart_height_ratio / 2)
    canvas.create_window(current_width / 2, chart_center_y, window=canvas_chart_widget, anchor="center")
    canvas_chart_widget_ref = canvas_chart_widget  # Store reference to the new widget

    # Position the savings label
    total_savings_y = current_height * (0.15 + chart_height_ratio) + 30
    canvas.create_window(current_width / 2, total_savings_y, window=total_savings_lbl,
                         anchor="n")  # Use total_savings_lbl

    plt.close(fig)  # Close the matplotlib figure to free memory


# Global variables for the category combobox in recent transactions
recent_transaction_category_combobox = None
recent_transaction_category_combobox_window_id = None  # To store the canvas window ID for the combobox

# Global reference for the "Add" button to prevent garbage collection
add_button_ref = None


def on_add_button_click():
    """Placeholder function for when the Add button is clicked."""
    print("Add new savings transaction clicked!")
    # Add your logic here to open a new window or form for adding savings transactions


def update_recent_transaction_box(event):
    """Updates the content of the right-side recent transactions box on resize."""
    global recent_transaction_category_combobox, recent_transaction_category_combobox_window_id, add_button_ref
    recent_transaction_canvas.delete("all")  # Clear previous drawings
    current_width = event.width
    current_height = event.height

    # 1. Draw the main rounded rectangle background
    draw_rounded_rect(recent_transaction_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR,
                      outline_width=0)

    # 2. Draw the peso sign watermark. It will be BEHIND anything drawn AFTER it.
    recent_transaction_canvas.create_text(current_width / 2, current_height / 2, text="₱",
                                          font=("Arial", int(current_height * 0.7), "bold"),
                                          fill="#f0f0e0", anchor="center", tags="watermark")  # Faded color
    recent_transaction_canvas.tag_lower("watermark")  # Ensures it's in the background

    # 3. Draw all other foreground content (headers, combobox, transaction list).
    # These will naturally appear ON TOP of the background and watermark because they are drawn last.

    # Header: "Recent Savings"
    recent_transaction_canvas.create_text(20, 20, anchor="nw", text="Recent Savings", font=FONT_SECTION,
                                          fill="black")

    # Add Button (text-based as per previous request)
    if add_button_ref is None or not add_button_ref.winfo_exists():
        add_button_ref = tk.Button(
            recent_transaction_canvas,
            text="+",
            font=("Arial", 14, "bold"),
            bg=COLOR_CANVAS_BAR,
            fg="black",
            relief="flat",
            command=on_add_button_click,
            width=2,
            height=1,
            borderwidth=0,
            highlightthickness=0
        )
        recent_transaction_canvas.create_window(current_width - 30, 20, window=add_button_ref, anchor="ne")
    else:
        recent_transaction_canvas.coords(add_button_ref, current_width - 30, 20)
        recent_transaction_canvas.tag_raise(add_button_ref)

    # Column Headers: "Amount" (Category is handled by the dropdown)
    recent_transaction_canvas.create_text(current_width - 30, 60, anchor="ne", text="Amount", font=FONT_SUBTEXT,
                                          fill="black")

    # Category Dropdown - Create/reposition it if its window ID exists
    if recent_transaction_category_combobox is None or not recent_transaction_category_combobox.winfo_exists():
        recent_transaction_category_combobox_var = tk.StringVar(value="Category")
        recent_transaction_category_combobox = ttk.Combobox(
            recent_transaction_canvas,
            textvariable=recent_transaction_category_combobox_var,
            values=["Category", "Deposit", "Withdrawal", "Interest", "Investment", "Transfer", "Miscellaneous"],
            # Updated values for savings
            state="readonly",
            width=10,
            font=FONT_SUBTEXT,
            justify="center"
        )
        # Aligned with "Recent Savings" text at x=20
        recent_transaction_category_combobox_window_id = recent_transaction_canvas.create_window(
            20, 60, window=recent_transaction_category_combobox, anchor="nw"
        )
    else:
        # Update its coordinates and raise it if it already exists
        recent_transaction_canvas.coords(recent_transaction_category_combobox_window_id, 20, 60)
        recent_transaction_canvas.tag_raise(recent_transaction_category_combobox_window_id)

    # Transaction list
    y_offset = 90
    line_height = 28
    for idx, (category, amount) in enumerate(transactions):
        if y_offset + line_height > current_height - 30:  # Prevent drawing beyond visible area
            break
        recent_transaction_canvas.create_text(30, y_offset, anchor="w", text=f"• {category}", font=FONT_TRANSACTION,
                                              fill="black")
        recent_transaction_canvas.create_text(current_width - 30, y_offset, anchor="e", text=f"{amount}",
                                              font=FONT_TRANSACTION, fill="black")
        y_offset += line_height


# --- Main App Window ---
def create_total_savings_app():
    root = tk.Tk()
    root.title("TrackU - Total Savings")
    root.state("zoomed")
    root.configure(bg=COLOR_BG)

    # --- Create a main frame to contain everything ---
    # This frame will occupy the entire root window and manage the grid.
    main_app_frame = tk.Frame(root, bg=COLOR_BG)
    main_app_frame.pack(fill="both", expand=True) # Use pack to make it fill the root window

    # --- MAIN APP FRAME GRID CONFIGURATION (NOW ON main_app_frame) ---
    # Corrected: grid_columnconfigure (no underscore after 'column')
    main_app_frame.grid_columnconfigure(0, weight=0, minsize=250)  # Sidebar column
    main_app_frame.grid_columnconfigure(1, weight=1)              # Main content column

    # Corrected: grid_rowconfigure (no underscore after 'row')
    main_app_frame.grid_rowconfigure(0, weight=0, minsize=85)     # Navbar row (taller)
    main_app_frame.grid_rowconfigure(1, weight=1)                 # Main content row

    # --- LEFT SIDEBAR FRAME (Spans both rows in column 0 of main_app_frame) ---
    sidebar_frame = tk.Frame(main_app_frame, bg=COLOR_SIDEBAR, width=250, highlightthickness=0)
    sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
    sidebar_frame.grid_propagate(False)  # Prevent frame from resizing to content

    # Corrected: grid_columnconfigure (no underscore after 'column')
    sidebar_frame.grid_columnconfigure(0, weight=1)

    # --- Sidebar Logo ---
    global sidebar_logo_img  # Keep a reference to the PhotoImage object
    sidebar_logo_img = None
    try:
        script_dir = os.path.dirname(__file__)
        logo_path_attempt = os.path.join(script_dir, "testlogo.png")
        if not os.path.exists(logo_path_attempt):
            logo_path_attempt = os.path.join(script_dir, "icons", "testlogo.png")  # Try in 'icons' folder too

        if os.path.exists(logo_path_attempt):
            img = Image.open(logo_path_attempt).resize(LOGO_SIZE_SIDEBAR, Image.LANCZOS)
            sidebar_logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(sidebar_frame, image=sidebar_logo_img, bg=COLOR_SIDEBAR, borderwidth=0)
            logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
        else:
            logo_label = tk.Label(sidebar_frame, text="TrackU Logo", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR,
                                  fg="darkgray")
            logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
            print("Warning: testlogo.png not found for sidebar. Using placeholder text.")
    except Exception as e:
        print(f"Error loading sidebar logo: {e}. Using placeholder text.")
        logo_label = tk.Label(sidebar_frame, text="TrackU Logo", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR,
                              fg="darkgray")
        logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")

    # Sidebar menu items - passing on_menu_item_click as the command
    sidebar_items_data = [
        ("Dashboard", "dashboard"),
        ("Total Expenses", "expenses"),
        ("Total Savings", "savings"),  # This page will be highlighted
        ("Profile", "profile")
    ]

    row_idx = 1  # Start creating sidebar items from row 1, after the logo (row 0)
    for text, icon_name in sidebar_items_data:
        create_sidebar_item(sidebar_frame, text, icon_name, row_idx,
                            command_func=lambda item=text: on_menu_item_click(item, root),
                            current_page_name="Total Savings")  # Pass current page name for highlighting
        row_idx += 1

    # Corrected: grid_rowconfigure (no underscore after 'row')
    sidebar_frame.grid_rowconfigure(row_idx, weight=1)  # Push sidebar items to the top

    # --- TOP RIGHT HEADER / NAVBAR (Canvas for drawing rounded bottom corners) ---
    global top_right_header_canvas
    top_right_header_canvas = tk.Canvas(main_app_frame, bg=COLOR_BG, height=85, highlightthickness=0)
    top_right_header_canvas.grid(row=0, column=1, sticky="nsew")
    top_right_header_canvas.bind("<Configure>", draw_top_right_header_content)

    # --- MAIN CONTENT FRAME (Placed in row 1, column 1, below the top right header) ---
    main_content_area = tk.Frame(main_app_frame, bg=COLOR_BG)
    main_content_area.grid(row=1, column=1, sticky="nsew", padx=30, pady=20)
    # Corrected: grid_columnconfigure (no underscore after 'column')
    main_content_area.grid_columnconfigure(0, weight=1, minsize=300)  # Left section (pie chart)
    main_content_area.grid_columnconfigure(1, weight=1)  # Right section (recent transactions)
    # Corrected: grid_rowconfigure (no underscore after 'row')
    main_content_area.grid_rowconfigure(0, weight=1)

    # --- LEFT SECTION: Pie Chart and Savings Details ---
    pie_chart_section_canvas = tk.Canvas(main_content_area, bg=COLOR_BG, highlightthickness=0)
    pie_chart_section_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=10)

    # --- MONTHS DROPDOWN (for Pie Chart Section) ---
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    month_var = tk.StringVar(value="June")  # Set current month to June 2025
    month_combo = ttk.Combobox(pie_chart_section_canvas, textvariable=month_var, values=months,
                               state="readonly", font=FONT_SUBTEXT, justify="center", width=10)
    month_combo.current(5)  # Set default selected month to June (index 5)

    total_savings_amount_lbl = tk.Label(pie_chart_section_canvas, text="Total Savings:\n₱ 100,000.00",
                                        font=("Georgia", 13), bg=COLOR_BG, fg="black", justify=tk.LEFT)

    pie_chart_section_canvas.bind("<Configure>",
                                  lambda event: update_pie_chart_section(event, pie_chart_section_canvas, month_combo,
                                                                         total_savings_amount_lbl))

    # --- RIGHT SECTION: Recent Savings ---
    global recent_transaction_canvas
    recent_transaction_canvas = tk.Canvas(main_content_area, bg=COLOR_BG, highlightthickness=0)
    recent_transaction_canvas.grid(row=0, column=1, sticky="nsew", pady=10)

    recent_transaction_canvas.bind("<Configure>", update_recent_transaction_box)

    root.mainloop()


if __name__ == "__main__":
    create_total_savings_app()