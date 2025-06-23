import tkinter as tk
from tkinter import ttk, messagebox
import pyglet
from PIL import Image, ImageTk
import os
import subprocess
import sys
from datetime import datetime
import calendar  # Import calendar module

# --- Path setup for database_manager.py ---
# Get the directory of the current script (dashboard.py is in DASHBOARD/)
current_script_dir = os.path.dirname(__file__)

# Go up one level (from DASHBOARD/ to Python Coding/)
# Then go into 'TOTAL EXPENSES' where database_manager.py is
database_folder_path = os.path.abspath(os.path.join(current_script_dir, "..", "TOTAL EXPENSES"))

# Add this path to sys.path
if database_folder_path not in sys.path:
    sys.path.append(database_folder_path)
# ------------------------------------------

# Import specific functions from database_manager
import database_manager # Keep the direct import for simplicity as requested

# Now you can directly call database_manager.get_username_by_id

# --- Global Font Loading ---
try:
    pyglet.font.add_file('Playfair Display.ttf')
except Exception as e:
    print(f"Warning: Could not load Playfair Display.ttf. Using default system fonts. Error: {e}")

# --- Colors ---
COLOR_BG = "#fdfdf5"
COLOR_NAVBAR = "#ffe0b2"
COLOR_SIDEBAR = "#d6e9d5"
COLOR_LINE = "#d3d3d3"
COLOR_CANVAS_BAR = "#fdf6e3"
COLOR_BOX_BORDER = "black"

# --- Fonts ---
FONT_BRAND = ("Playfair Display", 20, "bold")
FONT_MENU = ("Playfair Display", 13)
FONT_SECTION = ("Georgia", 16, "bold")
FONT_SUBTEXT = ("Playfair Display", 12)
FONT_AMOUNT = ("Georgia", 24, "underline")
FONT_TRANSACTION = ("Playfair Display", 11)
FONT_BUTTON = ("Arial", 25)
FONT_WELCOME = ("Playfair Display", 22, "bold")

BAR_COLOR = "#fdf6e3"  # Background of the bar chart canvas
BAR_FILL_COLOR = "#ffa726"  # Color of the actual bars

LOGO_SIZE_SIDEBAR = (150, 100)

# --- Global Tkinter StringVars for comboboxes ---
expense_month_var = None
savings_month_var = None

# --- Global references for main window and canvases ---
root_window = None
navbar_canvas_ref = None
left_expense_box_canvas_ref = None
left_savings_box_canvas_ref = None
right_transaction_canvas_ref = None

# --- Global references for the month combobox widgets (created once) ---
expense_month_combo_widget_ref = None
savings_month_combo_widget_ref = None

# --- Global references for labels within the boxes that update frequently ---
expense_amount_lbl_ref = None
savings_amount_lbl_ref = None
welcome_label_ref = None

# --- Global canvases for bar charts (created once) ---
expense_bar_canvas_ref = None
savings_bar_canvas_ref = None

# --- Global variable to store the logged-in user's ID and Username ---
logged_in_user_id = None # Changed default to None, as it will be passed from login
logged_in_username = "Guest" # Default value if no user is passed


def draw_bottom_rounded_rect(canvas, x, y, w, h, r, color):
    canvas.create_rectangle(x, y, x + w, y + r, fill=color, outline=color)
    canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)
    canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x + r, y + h - r, x + w - r, y + h, fill=color, outline=color)


def draw_rounded_rect(canvas, x, y, w, h, r, color):
    canvas.create_arc(x, y, x + 2 * r, y + 2 * r, start=90, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y, x + w, y + 2 * r, start=0, extent=90, fill=color, outline=color)
    canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color)
    canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)


def create_bar(canvas, data_values):
    canvas.delete("bar", "bar_labels")  # Delete previous bars and labels

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    if canvas_width <= 1 or canvas_height <= 1:
        return  # Avoid drawing on uninitialized canvas

    if not data_values or all(v == 0 for v in data_values):
        # Display a "No data" message
        canvas.create_text(canvas_width / 2, canvas_height / 2,
                           text="No data for this month.",
                           font=FONT_SUBTEXT, fill="gray", tags="bar_labels")
        return

    max_data_value = max(data_values)
    if max_data_value == 0:  # Should be caught by the above, but as a safeguard
        max_data_value = 1

    num_bars = len(data_values)

    # Calculate available space per bar (bar + spacing)
    # Give some padding on the left/right
    padding_x = 10
    total_drawable_width = canvas_width - 2 * padding_x

    space_per_bar = total_drawable_width / num_bars

    # Try to make bars a fixed width if possible, or scale if too many
    preferred_bar_width = 15  # pixels
    min_spacing = 5  # pixels

    # Calculate actual bar width and spacing
    actual_bar_width = min(preferred_bar_width, space_per_bar - min_spacing)
    if actual_bar_width <= 0:  # Fallback if bars are too tight
        actual_bar_width = space_per_bar * 0.7
        actual_spacing = space_per_bar * 0.3
    else:
        actual_spacing = space_per_bar - actual_bar_width

    x_start = padding_x + actual_spacing / 2  # Initial offset from the left edge

    # Y-axis padding for bars (top and bottom)
    padding_y_top = 20
    padding_y_bottom = 20
    drawable_height = canvas_height - padding_y_top - padding_y_bottom

    for i, height in enumerate(data_values):
        # Scale bar height relative to max_data_value and drawable height
        bar_height = (height / max_data_value) * drawable_height

        # Draw the bar from the bottom up
        y1 = canvas_height - padding_y_bottom - bar_height
        y2 = canvas_height - padding_y_bottom

        canvas.create_rectangle(x_start, y1, x_start + actual_bar_width, y2,
                                fill=BAR_FILL_COLOR, outline="", tags="bar")

        # Draw day label below the bar
        # Only show labels for every 5th day or if there are few days
        if num_bars <= 10 or (i + 1) % 5 == 0:
            day_num = i + 1  # Days are 1-indexed
            canvas.create_text(x_start + actual_bar_width / 2, canvas_height - 10,
                               text=str(day_num), font=("Arial", 8), fill="gray", tags="bar_labels")

        x_start += actual_bar_width + actual_spacing


def update_left_box_canvas(event, box_canvas, box_type):
    """
    Updates the content of the left-side section (month, total amount, bar chart).
    box_type can be 'expense' or 'saving'.
    """
    global expense_month_combo_widget_ref, savings_month_combo_widget_ref
    global expense_amount_lbl_ref, savings_amount_lbl_ref
    global expense_bar_canvas_ref, savings_bar_canvas_ref

    # Ensure canvases and widgets exist before proceeding
    if not box_canvas:
        return

    box_canvas.delete("all")  # Clear the canvas

    # Get current dimensions from the canvas, or use a default if event is None
    # For initial call from refresh_all_dashboard_data (event=None), get current dimensions
    # For <Configure> event, use event.width/height
    current_width = box_canvas.winfo_width() if event is None else event.width
    current_height = box_canvas.winfo_height() if event is None else event.height

    if current_width <= 1 or current_height <= 1:
        return  # Canvas not yet properly sized

    # Draw the main rounded rectangle background
    draw_rounded_rect(box_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR)

    # Determine which global variables to use based on box_type
    if box_type == 'expense':
        month_combo_ref = expense_month_combo_widget_ref
        amount_lbl_ref = expense_amount_lbl_ref
        bar_canvas_ref = expense_bar_canvas_ref
        title_text = "Total Expenses"
        month_var_instance = expense_month_var
        get_total_func = database_manager.get_total_expenses_by_month_year
        get_daily_func = database_manager.get_total_expenses_by_day_for_month_year
        box_tag = "expense_box"  # Tag for the bar canvas window
    elif box_type == 'saving':
        month_combo_ref = savings_month_combo_widget_ref
        amount_lbl_ref = savings_amount_lbl_ref
        bar_canvas_ref = savings_bar_canvas_ref
        title_text = "Total Savings"
        month_var_instance = savings_month_var
        get_total_func = database_manager.get_total_savings_by_month_year
        get_daily_func = database_manager.get_total_savings_by_day_for_month_year
        box_tag = "saving_box"  # Tag for the bar canvas window
    else:
        return  # Invalid box_type

    # Get selected month name, convert to number
    selected_month_name = month_var_instance.get()
    try:
        month_to_num = {name: i for i, name in enumerate(calendar.month_name) if i > 0}
        current_display_month_num = month_to_num.get(selected_month_name, datetime.now().month)
    except ValueError:
        current_display_month_num = datetime.now().month  # Fallback

    current_display_year = datetime.now().year  # Assuming current year for dashboard

    # --- Fetch Data ---
    total_amount = get_total_func(current_display_month_num, current_display_year)
    daily_data = get_daily_func(current_display_month_num, current_display_year)

    # --- Update UI Elements ---

    # Place the month combobox
    box_canvas.create_window(current_width / 2, 40, window=month_combo_ref, anchor="center")

    # Update and place amount label
    amount_lbl_ref.config(text=f"₱ {total_amount:,.2f}")
    box_canvas.create_window(20, 100, window=amount_lbl_ref, anchor="w")

    # Place title text
    box_canvas.create_text(20, 140, text=title_text, font=FONT_SECTION, fill="black", anchor="w")

    # Update and place bar canvas
    # Delete old window item for the bar canvas, if it exists (by tag)
    box_canvas.delete(f"{box_type}_bar_canvas_window")

    bar_canvas_x_pos = current_width * 0.65
    bar_canvas_y_pos = current_height * 0.55

    # Re-create the window for the bar_canvas_ref
    box_canvas.create_window(bar_canvas_x_pos, bar_canvas_y_pos, window=bar_canvas_ref,
                             anchor="center", tags=f"{box_type}_bar_canvas_window")

    # Configure the bar_canvas_ref dimensions (it's a child widget)
    bar_canvas_ref.config(width=int(current_width * 0.6), height=int(current_height * 0.5))

    # Now, draw bars on the bar_canvas_ref itself
    bar_canvas_ref.update_idletasks()  # Ensure it's sized before drawing bars
    create_bar(bar_canvas_ref, daily_data)


def update_right_canvas(event=None):  # event is optional now
    """
    Updates the content of the right-side recent transactions box.
    """
    global right_transaction_canvas_ref

    if not right_transaction_canvas_ref:
        return

    right_transaction_canvas_ref.delete("all")
    current_width = right_transaction_canvas_ref.winfo_width() if event is None else event.width
    current_height = right_transaction_canvas_ref.winfo_height() if event is None else event.height

    if current_width <= 1 or current_height <= 1:
        return  # Canvas not yet properly sized

    draw_rounded_rect(right_transaction_canvas_ref, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR)
    right_transaction_canvas_ref.create_text(20, 20, anchor="nw", text="Recent Transactions", font=FONT_SECTION,
                                             fill="black")
    right_transaction_canvas_ref.create_text(current_width - 30, 60, anchor="ne", text="Amount", font=FONT_SUBTEXT,
                                             fill="black")
    right_transaction_canvas_ref.create_text(20, 60, anchor="nw", text="Category & Date", font=FONT_SUBTEXT,
                                             fill="black")

    # Fetch recent transactions (combined expenses and savings)
    recent_transactions = database_manager.get_recent_combined_transactions(limit=10)  # Get top 10

    y_offset = 100
    line_height = 28
    display_limit = int((current_height - y_offset - 30) / line_height)  # Max items that can fit

    if not recent_transactions:
        right_transaction_canvas_ref.create_text(
            current_width / 2, y_offset + line_height,
            anchor="center",
            text="No Recent Transactions",
            font=FONT_SUBTEXT,
            fill="gray"
        )
    else:
        for idx, (trans_date_str, trans_type, category, amount, notes) in enumerate(recent_transactions):
            if idx >= display_limit:
                break

            try:
                dt_obj = datetime.strptime(trans_date_str, "%Y-%m-%d %H:%M:%S")
                display_date = dt_obj.strftime("%b %d, %Y")
            except ValueError:
                display_date = "Invalid Date"

            # Determine color based on transaction type
            amount_color = "red" if trans_type == "Expense" else "green"
            display_amount = f"₱{amount:,.2f}"
            if trans_type == "Expense":
                display_amount = f"-{display_amount}"
            # No explicit '+' for savings, as it's implied positive. If you want it, add:
            # else:
            #      display_amount = f"+{display_amount}"

            display_text = f"• {category} ({display_date})"

            right_transaction_canvas_ref.create_text(30, y_offset, anchor="w", text=display_text, font=FONT_TRANSACTION,
                                                     fill="black")
            right_transaction_canvas_ref.create_text(current_width - 30, y_offset, anchor="e", text=display_amount,
                                                     font=FONT_TRANSACTION, fill=amount_color)
            y_offset += line_height


def draw_navbar_content(event):
    """Draws the custom rounded rectangle and places content on the top right header canvas."""
    global navbar_canvas_ref
    navbar_canvas_ref.delete("all")
    draw_bottom_rounded_rect(navbar_canvas_ref, 0, 0, event.width, event.height, 20, COLOR_NAVBAR)

    brand_label = tk.Label(navbar_canvas_ref, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
    navbar_canvas_ref.create_window(20, event.height / 2, window=brand_label, anchor="w")

    dashboard_title_label = tk.Label(navbar_canvas_ref, text="Dashboard", font=("Georgia", 16), bg=COLOR_NAVBAR,
                                     fg="#222")
    navbar_canvas_ref.create_window(event.width - 30, event.height / 2, window=dashboard_title_label, anchor="e")


def on_menu_item_click(item_name):
    """Handles the click event for sidebar menu items."""
    print(f"'{item_name}' was clicked!")

    global root_window, logged_in_user_id

    current_dashboard_dir = os.path.dirname(__file__)
    script_to_launch = None

    if item_name == "Dashboard":
        script_to_launch = os.path.join(current_dashboard_dir, "dashboard.py")
        # If already on dashboard, just refresh instead of relaunching/destroying
        if os.path.abspath(sys.argv[0]) == os.path.abspath(script_to_launch):
            print("Already on Dashboard page, refreshing data.")
            refresh_all_dashboard_data()
            return
    elif item_name == "Total Expenses":
        # Path to expenses.py within TOTAL EXPENSES folder
        script_to_launch = os.path.join(current_dashboard_dir, "..", "TOTAL EXPENSES", "expenses.py")
    elif item_name == "Total Savings":
        # Path to savings.py within TOTAL SAVINGS folder
        script_to_launch = os.path.join(current_dashboard_dir, "..", "TOTAL SAVINGS",
                                        "savings.py")  # Corrected to savings.py
    elif item_name == "Profile":
        messagebox.showinfo("Profile", "Profile functionality coming soon!")
        return  # Don't close window for this

    if script_to_launch:
        try:
            # First, destroy the current window
            if root_window and root_window.winfo_exists():
                root_window.destroy()

            # Then, launch the new script
            cmd = [sys.executable, script_to_launch]
            if logged_in_user_id is not None: # Pass user ID if available
                cmd.append(str(logged_in_user_id))

            if sys.platform.startswith('win'):
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(cmd)  # For Linux/macOS

            print(f"Launched: {script_to_launch}")
        except FileNotFoundError:
            messagebox.showerror("Launch Error", "Python interpreter not found. Ensure Python is in your PATH.")
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch {script_to_launch}:\n{e}")


def refresh_all_dashboard_data(event=None):
    """Refreshes all dynamic data on the dashboard. Called on month change or initial load."""
    global left_expense_box_canvas_ref, left_savings_box_canvas_ref, right_transaction_canvas_ref

    # Ensure canvases exist and are mapped before calling updates
    # We call update_idletasks before getting dimensions inside the update functions

    # Update Expense Box
    if left_expense_box_canvas_ref and left_expense_box_canvas_ref.winfo_exists():
        update_left_box_canvas(None, left_expense_box_canvas_ref, 'expense')

    # Update Savings Box
    if left_savings_box_canvas_ref and left_savings_box_canvas_ref.winfo_exists():
        update_left_box_canvas(None, left_savings_box_canvas_ref, 'saving')

    # Update Recent Transactions Box
    if right_transaction_canvas_ref and right_transaction_canvas_ref.winfo_exists():
        update_right_canvas(None)


def create_dashboard_app():
    global root_window, navbar_canvas_ref, left_expense_box_canvas_ref, left_savings_box_canvas_ref, right_transaction_canvas_ref
    global expense_month_var, savings_month_var
    global expense_month_combo_widget_ref, savings_month_combo_widget_ref
    global expense_amount_lbl_ref, savings_amount_lbl_ref
    global expense_bar_canvas_ref, savings_bar_canvas_ref
    global welcome_label_ref
    global logged_in_user_id, logged_in_username

    root_window = tk.Tk()
    root_window.title("TrackU Dashboard")
    root_window.state("zoomed")  # Start maximized
    root_window.configure(bg=COLOR_BG)

    # Initialize the database
    database_manager.initialize_db()

    # --- Retrieve User ID from command line arguments ---
    if len(sys.argv) > 1:
        try:
            logged_in_user_id = int(sys.argv[1])
            # Fetch username using the ID
            fetched_username = database_manager.get_username_by_id(logged_in_user_id)
            if fetched_username:
                logged_in_username = fetched_username
            else:
                print(f"Warning: User with ID {logged_in_user_id} not found in database. Using default 'Guest'.")
        except ValueError:
            print("Error: Invalid user ID provided as command-line argument. Using default 'Guest'.")
            logged_in_user_id = None # Ensure it's None if conversion fails
    else:
        print("No user ID provided as command-line argument. Running as guest or default user.")
        # If no ID is provided, you might want to try to get a default user or prompt for login
        # For this scenario, we'll keep it as "Guest" and logged_in_user_id as None.

    # --- Grid Configuration for main window ---
    root_window.grid_columnconfigure(0, weight=0, minsize=250)  # Sidebar column
    root_window.grid_columnconfigure(1, weight=1)  # Main content column
    root_window.grid_rowconfigure(0, weight=0, minsize=85)  # Navbar row
    root_window.grid_rowconfigure(1, weight=1)  # Main content area row

    # --- Initialize global StringVars for comboboxes ---
    current_month_name = calendar.month_name[datetime.now().month]
    expense_month_var = tk.StringVar(value=current_month_name)
    savings_month_var = tk.StringVar(value=current_month_name)

    # --- LEFT SIDEBAR FRAME ---
    sidebar_frame = tk.Frame(root_window, bg=COLOR_SIDEBAR, width=250, highlightthickness=0)  # Set fixed width
    sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
    sidebar_frame.grid_propagate(False)  # Prevent frame from shrinking to fit contents
    sidebar_frame.grid_columnconfigure(0, weight=1)

    global sidebar_logo_img  # Keep reference to avoid garbage collection
    sidebar_logo_img = None
    try:
        # Adjusted path logic to be relative to the script's directory
        script_dir = os.path.dirname(__file__)
        logo_path_attempt = os.path.join(script_dir, "testlogo.png")
        if not os.path.exists(logo_path_attempt):  # If not in current dir, check 'icons' subdir
            logo_path_attempt = os.path.join(script_dir, "icons", "testlogo.png")

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

    menu_items = ["", "", "Dashboard", "Total Expenses", "Total Savings", "", "", "", "", "", "Profile"]

    row_idx = 1
    for item in menu_items:
        if item:
            # Add separator before items, except for the first actual item
            if row_idx > 1 and item not in ["Dashboard"]:  # Don't add separator before first item or after last dummy
                prev_item_index = menu_items.index(item) - 1
                if prev_item_index >= 0 and menu_items[prev_item_index] != "":  # Check if previous item was not empty
                    separator_frame = tk.Frame(sidebar_frame, bg=COLOR_BOX_BORDER, height=1)
                    separator_frame.grid(row=row_idx, column=0, sticky="ew", padx=10, pady=(5, 5))
                    row_idx += 1

            menu_button = tk.Button(
                sidebar_frame,
                text=item,
                font=FONT_MENU,
                bg=COLOR_SIDEBAR,
                fg="black",
                command=lambda i=item: on_menu_item_click(i),
                relief="flat",
                activebackground=COLOR_NAVBAR,
                anchor="w",
                padx=15
            )
            # Highlight Dashboard button as it's the current page
            if item == "Dashboard":
                menu_button.config(bg=COLOR_NAVBAR)

            # Hover effects
            def _on_enter(event, btn=menu_button, current=item, current_page="Dashboard"):
                if current != current_page:
                    btn.config(bg="#e0e0e0")

            def _on_leave(event, btn=menu_button, current=item, current_page="Dashboard"):
                if current != current_page:
                    btn.config(bg=COLOR_SIDEBAR)

            menu_button.bind("<Enter>", _on_enter)
            menu_button.bind("<Leave>", _on_leave)

            menu_button.grid(row=row_idx, column=0, pady=5, sticky="ew")
            row_idx += 1
        else:  # Handle empty strings for spacing
            if item == "" and "Profile" in menu_items and menu_items.index("Profile") == menu_items.index(item) + 1:
                # This empty label ensures the profile button goes to the bottom
                sidebar_frame.grid_rowconfigure(row_idx, weight=1)
            tk.Label(sidebar_frame, text="", bg=COLOR_SIDEBAR).grid(row=row_idx, column=0, pady=0)
            row_idx += 1

    sidebar_frame.grid_rowconfigure(row_idx, weight=1)  # Push content up

    # --- TOP RIGHT HEADER / NAVBAR ---
    navbar_canvas_ref = tk.Canvas(root_window, bg=COLOR_BG, height=85, highlightthickness=0)
    navbar_canvas_ref.grid(row=0, column=1, sticky="nsew")
    navbar_canvas_ref.bind("<Configure>", draw_navbar_content)

    # --- MAIN CONTENT FRAME ---
    main_content_area = tk.Frame(root_window, bg=COLOR_BG)
    main_content_area.grid(row=1, column=1, sticky="nsew", padx=30, pady=20)
    main_content_area.grid_columnconfigure(0, weight=1, minsize=300)  # Left Column
    main_content_area.grid_columnconfigure(1, weight=1)  # Right Column
    main_content_area.grid_rowconfigure(0, weight=0)  # Welcome label row
    main_content_area.grid_rowconfigure(1, weight=1)  # Boxes row

    # Welcome Label (now updated with username)
    welcome_label_ref = tk.Label(main_content_area, text=f"Welcome, {logged_in_username}", font=FONT_WELCOME, bg=COLOR_BG)
    welcome_label_ref.grid(row=0, column=0, columnspan=2, sticky="w", padx=(0, 0), pady=(0, 10))

    # --- BOXES CONTAINER FRAME (holds left and right boxes) ---
    boxes_container_frame = tk.Frame(main_content_area, bg=COLOR_BG)
    boxes_container_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
    boxes_container_frame.grid_columnconfigure(0, weight=1)  # Left boxes column
    boxes_container_frame.grid_columnconfigure(1, weight=1)  # Right box column
    boxes_container_frame.grid_rowconfigure(0, weight=1)  # Single row for boxes

    # --- LEFT SECTION: Expense and Savings Boxes ---
    left_boxes_frame = tk.Frame(boxes_container_frame, bg=COLOR_BG)
    left_boxes_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
    left_boxes_frame.grid_rowconfigure((0, 1), weight=1)  # Two rows for two boxes
    left_boxes_frame.grid_columnconfigure(0, weight=1)

    # Expense Box Canvas
    left_expense_box_canvas_ref = tk.Canvas(left_boxes_frame, bg=COLOR_BG, highlightthickness=0)
    left_expense_box_canvas_ref.grid(row=0, column=0, pady=15, sticky="nsew")

    # Expense Month Combobox (CREATED ONCE)
    months = [calendar.month_name[i] for i in range(1, 13)]
    expense_month_combo_widget_ref = ttk.Combobox(left_expense_box_canvas_ref, textvariable=expense_month_var,
                                                  values=months,
                                                  state="readonly", font=FONT_SUBTEXT, justify="center", width=15)
    expense_month_combo_widget_ref.current(datetime.now().month - 1)
    expense_month_combo_widget_ref.bind("<<ComboboxSelected>>", refresh_all_dashboard_data)  # Re-bind to refresh all

    # Expense Amount Label (CREATED ONCE)
    expense_amount_lbl_ref = tk.Label(left_expense_box_canvas_ref, text="₱ 0.00", font=FONT_AMOUNT, bg=COLOR_CANVAS_BAR,
                                      fg="black", anchor="w")

    # Expense Bar Canvas (CREATED ONCE as a child of left_expense_box_canvas_ref)
    expense_bar_canvas_ref = tk.Canvas(left_expense_box_canvas_ref, bg=COLOR_CANVAS_BAR, highlightthickness=0)
    # This bar_canvas_ref will be placed as a window on left_expense_box_canvas_ref when update_left_box_canvas runs.

    # Bind the outer canvas to configure event to trigger its update function
    left_expense_box_canvas_ref.bind("<Configure>",
                                     lambda event: update_left_box_canvas(event, left_expense_box_canvas_ref,
                                                                          'expense'))

    # Savings Box Canvas
    left_savings_box_canvas_ref = tk.Canvas(left_boxes_frame, bg=COLOR_BG, highlightthickness=0)
    left_savings_box_canvas_ref.grid(row=1, column=0, pady=15, sticky="nsew")

    # Savings Month Combobox (CREATED ONCE)
    savings_month_combo_widget_ref = ttk.Combobox(left_savings_box_canvas_ref, textvariable=savings_month_var,
                                                  values=months,
                                                  state="readonly", font=FONT_SUBTEXT, justify="center", width=15)
    savings_month_combo_widget_ref.current(datetime.now().month - 1)
    savings_month_combo_widget_ref.bind("<<ComboboxSelected>>", refresh_all_dashboard_data)  # Re-bind to refresh all

    # Savings Amount Label (CREATED ONCE)
    savings_amount_lbl_ref = tk.Label(left_savings_box_canvas_ref, text="₱ 0.00", font=FONT_AMOUNT, bg=COLOR_CANVAS_BAR,
                                      fg="black", anchor="w")

    # Savings Bar Canvas (CREATED ONCE as a child of left_savings_box_canvas_ref)
    savings_bar_canvas_ref = tk.Canvas(left_savings_box_canvas_ref, bg=COLOR_CANVAS_BAR, highlightthickness=0)

    # Bind the outer canvas to configure event to trigger its update function
    left_savings_box_canvas_ref.bind("<Configure>",
                                     lambda event: update_left_box_canvas(event, left_savings_box_canvas_ref, 'saving'))

    # --- RIGHT SECTION: Recent Transactions ---
    right_transaction_canvas_ref = tk.Canvas(boxes_container_frame, bg=COLOR_BG, highlightthickness=0)
    right_transaction_canvas_ref.grid(row=0, column=1, sticky="nsew", padx=(10, 10), pady=14)
    right_transaction_canvas_ref.bind("<Configure>", update_right_canvas)  # Pass only event, uses global ref

    # Initial data load and UI refresh
    root_window.update_idletasks()  # Ensure widgets have initial sizes before data is loaded
    refresh_all_dashboard_data()  # Perform initial data load and UI update

    root_window.mainloop()


if __name__ == "__main__":
    create_dashboard_app()