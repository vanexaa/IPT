import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import pyglet
import os
import subprocess
import sys
from datetime import datetime
import calendar

# --- Import your database manager ---
# Assuming database_manager.py is in the same directory as expenses.py
# If it's in a different folder, you'd need sys.path adjustments here too.
import database_manager

# ------------------------------------

try:
    pyglet.font.add_file('Playfair Display.ttf')
except Exception as e:
    print(f"Warning: Could not load Playfair Display.ttf. Using default system fonts. Error: {e}")

# --- Colors ---
COLOR_BG = "#fdfdf5"
COLOR_NAVBAR = "#ffe0b2"
COLOR_SIDEBAR = "#d6e9d5"
COLOR_CANVAS_BAR = "#fdf6e3"
COLOR_PIE_SLICE_1 = "#aed581"
COLOR_PIE_SLICE_2 = "#ffab91"
COLOR_PIE_SLICE_3 = "#b39ddb"
COLOR_PIE_SLICE_4 = "#f0e68c"
COLOR_PIE_SLICE_5 = "#87ceeb"
COLOR_BOX_BORDER = "black"

# --- Fonts ---
FONT_BRAND = ("Playfair Display", 20, "bold")
FONT_MENU = ("Playfair Display", 13)
FONT_SECTION = ("Georgia", 16, "bold")
FONT_SUBTEXT = ("Playfair Display", 12)
FONT_TRANSACTION = ("Playfair Display", 11)

LOGO_SIZE_SIDEBAR = (150, 100)

# Global references for labels in the header to prevent garbage collection
tracku_label_tk = None
total_expenses_header_label_tk = None
canvas_chart_widget_ref = None # For Matplotlib FigureCanvasTkAgg widget

# --- Global Tkinter StringVars for comboboxes (crucial for persistence) ---
month_var = None
recent_transaction_category_combobox_var = None
# -------------------------------------------------------------------------

# --- NEW Global References for Tkinter Widgets ---
# These will hold the actual Tkinter widget instances for persistent access
month_combo_widget_ref = None
total_expenses_amount_lbl_widget_ref = None

# Global references for recent transaction box widgets
recent_transaction_category_combobox = None # This will now be created once globally
recent_transaction_category_combobox_window_id = None # Its window ID
add_transaction_button = None # This will now be created once globally
add_transaction_button_window_id = None # Its window ID
# -------------------------------------------------

# Global variables to store current month/year for filtering
current_display_month_num = datetime.now().month
current_display_year = datetime.now().year

# --- Global reference for the child process launched by on_add_button_click ---
child_process_ref = None
# --- Global reference to the main Tkinter root window ---
root_window = None


def on_menu_item_click(item_name, current_root_param):
    """Handles the click event for sidebar menu items."""
    script_dir = os.path.dirname(__file__)
    script_to_launch = None
    if item_name == "Dashboard":
        script_to_launch = os.path.join(script_dir, "..", "DASHBOARD", "dashboard.py")
    elif item_name == "Total Expenses":
        print("Total Expenses clicked! (Currently on this page)")
        return
    elif item_name == "Total Savings":
        script_to_launch = os.path.join(script_dir, "..", "TOTAL SAVINGS", "savings.py")
    elif item_name == "Profile":
        print("Profile clicked!")
        return

    if script_to_launch:
        try:
            subprocess.Popen([sys.executable, script_to_launch])
            if item_name != "Total Expenses":
                current_root_param.destroy()
        except Exception as e:
            print(f"Failed to launch {script_to_launch}: {e}")


def draw_bottom_rounded_rect(canvas, x, y, w, h, r, color):
    """Draws a rectangle with rounded bottom corners on a Tkinter canvas."""
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
    else:
        canvas.create_arc(x, y, x + 2 * r, y + 2 * r, start=90, extent=90, fill=color, outline=color)
        canvas.create_arc(x + w - 2 * r, y, x + w, y + 2 * r, start=0, extent=90, fill=color, outline=color)
        canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color)
        canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
        canvas.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color)
        canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)


def draw_top_right_header_content(event):
    """Draws content on the top right header canvas."""
    global tracku_label_tk, total_expenses_header_label_tk
    top_right_header_canvas.delete("all")
    draw_bottom_rounded_rect(top_right_header_canvas, 0, 0, event.width, event.height, 20, COLOR_NAVBAR)

    if tracku_label_tk is None:
        tracku_label_tk = tk.Label(top_right_header_canvas, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
        total_expenses_header_label_tk = tk.Label(top_right_header_canvas, text="Total Expenses", font=("Georgia", 16),
                                                  bg=COLOR_NAVBAR, fg="#222")

    top_right_header_canvas.create_window(30, event.height / 2, window=tracku_label_tk, anchor="w")
    top_right_header_canvas.create_window(event.width - 30, event.height / 2, window=total_expenses_header_label_tk,
                                          anchor="e")


def on_add_button_click():
    """Launches the Expenses-Categories.py script in a new window."""
    global child_process_ref  # Declare global here
    script_dir = os.path.dirname(__file__)
    script_to_launch = os.path.join(script_dir, "Expenses-Categories.py")

    if os.path.exists(script_to_launch):
        try:
            # Launch the script without a new console window
            child_process_ref = subprocess.Popen([sys.executable, script_to_launch])
            print(f"Launched {script_to_launch}")
            # Start polling for child process exit
            root_window.after(100, check_child_process_status)  # Check every 100ms
        except Exception as e:
            print(f"Failed to launch {script_to_launch}: {e}")
    else:
        print(f"Error: {script_to_launch} not found. Please create this file.")


def check_child_process_status():
    """
    Periodically checks if the launched child process has exited.
    If it has, triggers a UI refresh.
    """
    global child_process_ref
    if child_process_ref and child_process_ref.poll() is None:
        # Process is still running, check again soon
        root_window.after(100, check_child_process_status)
    elif child_process_ref and child_process_ref.poll() is not None:
        # Process has exited, refresh UI
        print("Child process exited. Refreshing UI.")
        # Call refresh_data_and_ui directly
        refresh_data_and_ui()
        child_process_ref = None  # Clear reference
    else:
        # No child process launched or already handled
        pass


def refresh_data_and_ui():
    """
    Function to call when data needs to be refreshed (e.g., after adding a transaction
    or changing a filter). This will trigger a re-draw of the pie chart and recent transactions.
    """
    # Directly call the update functions, which will now use global widget references
    update_pie_chart_section()
    update_recent_transaction_box()


def update_pie_chart_section(event=None):
    """
    Updates the pie chart and associated elements by fetching data from the database.
    This function now uses global widget references for the combobox and label.
    """
    global canvas_chart_widget_ref, current_display_month_num, current_display_year
    global month_combo_widget_ref, total_expenses_amount_lbl_widget_ref # Access global refs

    # Ensure canvases exist before proceeding
    if not pie_chart_section_canvas or not month_combo_widget_ref or not total_expenses_amount_lbl_widget_ref:
        return

    pie_chart_section_canvas.delete("all") # Clear canvas but not the widgets placed by create_window

    # Get current dimensions from the canvas, or use a default if event is None
    if event:
        current_width = event.width
        current_height = event.height
    else:
        current_width = pie_chart_section_canvas.winfo_width()
        current_height = pie_chart_section_canvas.winfo_height()
        if current_width == 1 or current_height == 1:
             return

    # Watermark
    pie_chart_section_canvas.create_text(current_width / 2, current_height / 2, text="₱",
                       font=("Arial", int(current_height * 0.7), "bold"), fill="#f0f0f0", anchor="center",
                       tags="pie_watermark")
    pie_chart_section_canvas.tag_lower("")

    # Get selected month name, convert to number using the global widget reference
    selected_month_name = month_combo_widget_ref.get()
    try:
        month_to_num = {name: i for i, name in enumerate(calendar.month_name) if i > 0}
        current_display_month_num = month_to_num.get(selected_month_name, datetime.now().month)
    except ValueError:
        current_display_month_num = datetime.now().month

    current_display_year = datetime.now().year

    # Re-place the month combobox on the canvas (it might have been deleted by canvas.delete("all"))
    # The widget itself is globally referenced, so it's not destroyed, just its representation on canvas.
    pie_chart_section_canvas.create_window(current_width / 2, 40, window=month_combo_widget_ref, anchor="n")

    # --- Fetch data from database for Pie Chart ---
    expense_breakdown = database_manager.get_expense_breakdown_by_month_year(current_display_month_num,
                                                                             current_display_year)
    total_expenses_for_month = database_manager.get_total_expenses_by_month_year(current_display_month_num,
                                                                                 current_display_year)

    # Matplotlib Pie Chart setup
    chart_height_ratio = 0.6
    fig, ax = plt.subplots(figsize=(current_width / 100, (current_height * chart_height_ratio) / 100), dpi=100,
                           facecolor=COLOR_BG)

    # --- Handle cases with no expenses or zero total expenses ---
    if not expense_breakdown or total_expenses_for_month <= 0:
        labels = ["No Expenses"]
        sizes = [1]
        center_text = f"No Expenses This Month\n(for {selected_month_name} {current_display_year})"
        total_expenses_for_month = 0.0

        ax.text(0.5, 0.5, center_text,
                horizontalalignment='center', verticalalignment='center',
                fontsize=FONT_SECTION[1] + 2, color='gray', transform=ax.transAxes)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_facecolor(COLOR_BG)

    else:
        labels = [item[0] for item in expense_breakdown]
        sizes = [item[1] for item in expense_breakdown]

        pie_colors = [COLOR_PIE_SLICE_1, COLOR_PIE_SLICE_2, COLOR_PIE_SLICE_3, COLOR_PIE_SLICE_4, COLOR_PIE_SLICE_5,
                      "#cccccc", "#ffcc00", "#99ff99"]
        actual_colors = [pie_colors[i % len(pie_colors)] for i in range(len(sizes))]

        explode = [0.02] * len(sizes)

        # Draw pie chart with actual data
        wedges, texts, autotexts = ax.pie(sizes, colors=actual_colors, explode=explode, startangle=140,
                                          wedgeprops=dict(width=0.8, edgecolor=COLOR_BG), autopct='%1.1f%%',
                                          pctdistance=0.85)

        for text in texts:
            text.set_color('black')
            text.set_fontsize(FONT_SUBTEXT[1])

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(FONT_SUBTEXT[1] - 2)

        ax.axis('equal')
        ax.set_facecolor(COLOR_BG)
        plt.tight_layout(pad=0)

        if len(labels) > 0:
            ax.legend(wedges, labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
                      frameon=False, fontsize=FONT_SUBTEXT[1], title_fontsize=FONT_SECTION[1])

        center_text = f"\nTotal: ₱{total_expenses_for_month:,.2f}"

        ax.text(0, 0, center_text, horizontalalignment='center', verticalalignment='center',
                fontsize=FONT_SECTION[1], color='gray', transform=ax.transAxes)

    # Embed matplotlib chart into Tkinter canvas
    if canvas_chart_widget_ref:
        canvas_chart_widget_ref.destroy()

    canvas_chart_agg = FigureCanvasTkAgg(fig, master=pie_chart_section_canvas)
    canvas_chart_widget = canvas_chart_agg.get_tk_widget()
    canvas_chart_widget.config(bg=COLOR_BG)
    chart_center_y = current_height * (0.15 + chart_height_ratio / 2)
    pie_chart_section_canvas.create_window(current_width / 2, chart_center_y, window=canvas_chart_widget, anchor="center")
    canvas_chart_widget_ref = canvas_chart_widget

    # Update total expenses label (always update regardless of pie chart)
    total_expenses_amount_lbl_widget_ref.config(text=f"Total Expenses:\n₱ {total_expenses_for_month:,.2f}")
    total_expenses_y = current_height * (0.15 + chart_height_ratio) + 30
    pie_chart_section_canvas.create_window(current_width / 2, total_expenses_y, window=total_expenses_amount_lbl_widget_ref, anchor="n")

    plt.close(fig)


def update_recent_transaction_box(event=None):
    """
    Updates the content and layout of the recent transactions box
    by fetching data from the database.
    This function now ensures the combobox and add button persist.
    """
    global recent_transaction_category_combobox, recent_transaction_category_combobox_window_id, add_transaction_button, add_transaction_button_window_id, recent_transaction_category_combobox_var

    if not recent_transaction_canvas:
        return

    # !!! CRITICAL CHANGE: Only delete specific items, not "all" !!!
    # Delete previous transaction list items and watermark, but preserve combobox and button
    recent_transaction_canvas.delete("transaction_item")
    recent_transaction_canvas.delete("watermark") # Watermark also needs to be redrawn if canvas.delete("all") is removed
    recent_transaction_canvas.delete("static_text") # Delete titles too if they are part of redrawing

    # Get current dimensions from the canvas, or use a default if event is None
    if event:
        current_width = event.width
        current_height = event.height
    else:
        current_width = recent_transaction_canvas.winfo_width()
        current_height = recent_transaction_canvas.winfo_height()
        if current_width == 1 or current_height == 1:
            return

    # Draw the rounded rectangle background (this needs to be done every time if 'all' is removed)
    draw_rounded_rect(recent_transaction_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR,
                      outline_width=0)


    # Watermark (re-create as it was deleted)
    recent_transaction_canvas.create_text(current_width / 2, current_height / 2, text="₱",
                                          font=("Arial", int(current_height * 0.7), "bold"), fill="#f0f0f0",
                                          anchor="center", tags="watermark")
    recent_transaction_canvas.tag_lower("watermark")


    # "Recent Expenses" title (re-create as it was deleted or move its creation)
    recent_transaction_canvas.create_text(20, 20, anchor="nw", text="Recent Expenses", font=FONT_SECTION, fill="black", tags="static_text")

    # "Amount" header (re-create as it was deleted or move its creation)
    recent_transaction_canvas.create_text(current_width - 30, 60, anchor="ne", text="Amount", font=FONT_SUBTEXT,
                                          fill="black", tags="static_text")

    # The add_transaction_button and recent_transaction_category_combobox
    # are now created ONCE in create_total_expenses_app,
    # so we just need to ensure their position on the canvas is correct and update their content if needed.

    # Update combobox values in case new categories were added (e.g. from Expenses-Categories.py)
    categories_from_db = sorted(list(set(item[0] for item in database_manager.get_all_expenses())))
    categories_for_filter = ["All Categories"] + categories_from_db
    recent_transaction_category_combobox['values'] = categories_for_filter
    # Ensure the current selection is still valid after updating values
    if recent_transaction_category_combobox_var.get() not in categories_for_filter:
        recent_transaction_category_combobox_var.set("All Categories")

    # Ensure positions are updated on resize (these are canvas window items)
    recent_transaction_canvas.coords(add_transaction_button_window_id, current_width - 30, 20)
    recent_transaction_canvas.coords(recent_transaction_category_combobox_window_id, 30, 60)

    recent_transaction_canvas.tag_raise(add_transaction_button_window_id)
    recent_transaction_canvas.tag_raise(recent_transaction_category_combobox_window_id)


    # --- Fetch recent expenses from database and apply filter ---
    selected_filter_category = recent_transaction_category_combobox_var.get()
    all_expenses = database_manager.get_all_expenses()

    if selected_filter_category != "All Categories":
        filtered_expenses = [exp for exp in all_expenses if exp[0] == selected_filter_category]
    else:
        filtered_expenses = all_expenses

    y_offset = 90
    line_height = 28
    display_limit = int((current_height - y_offset - 30) / line_height)

    # Display "No Recent Expenses" if list is empty
    if not filtered_expenses:
        recent_transaction_canvas.create_text(
            current_width / 2, y_offset + line_height,
            anchor="center",
            text="No Recent Expenses",
            font=FONT_SUBTEXT,
            fill="gray",
            tags="transaction_item" # Tag this so it can be deleted next time
        )
    else:
        for idx, (category, amount, transaction_date_str) in enumerate(filtered_expenses):
            if idx >= display_limit:
                break

            display_amount = f"₱{amount:,.2f}"

            try:
                dt_obj = datetime.strptime(transaction_date_str, "%Y-%m-%d %H:%M:%S")
                display_date = dt_obj.strftime("%b %d, %Y")
            except ValueError:
                display_date = "Invalid Date"

            display_text = f"• {category} ({display_date})"

            # Add "transaction_item" tag to these elements
            recent_transaction_canvas.create_text(30, y_offset, anchor="w", text=display_text, font=FONT_TRANSACTION,
                                                  fill="black", tags="transaction_item")
            recent_transaction_canvas.create_text(current_width - 30, y_offset, anchor="e", text=display_amount,
                                                  font=FONT_TRANSACTION, fill="black", tags="transaction_item")
            y_offset += line_height


def create_total_expenses_app():
    """Creates and runs the main Total Expenses application window."""
    global root_window, month_var, recent_transaction_category_combobox_var
    global pie_chart_section_canvas, recent_transaction_canvas, top_right_header_canvas
    global month_combo_widget_ref, total_expenses_amount_lbl_widget_ref
    global recent_transaction_category_combobox, recent_transaction_category_combobox_window_id, add_transaction_button, add_transaction_button_window_id

    root_window = tk.Tk()
    root_window.title("TrackU - Total Expenses")
    root_window.state("zoomed")
    root_window.configure(bg=COLOR_BG)

    # --- Initialize global StringVars BEFORE widgets are created ---
    month_var = tk.StringVar(value=calendar.month_name[datetime.now().month])
    recent_transaction_category_combobox_var = tk.StringVar(value="All Categories")
    # ---------------------------------------------------------------

    database_manager.initialize_db()  # Initialize the database

    root_window.grid_columnconfigure(0, weight=0, minsize=250)
    root_window.grid_columnconfigure(1, weight=1)
    root_window.grid_rowconfigure(0, weight=0, minsize=85)
    root_window.grid_rowconfigure(1, weight=1)

    # --- Sidebar Frame ---
    sidebar_frame = tk.Frame(root_window, bg=COLOR_SIDEBAR, width=250, highlightthickness=0)
    sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
    sidebar_frame.grid_propagate(False)
    sidebar_frame.grid_columnconfigure(0, weight=1)

    global sidebar_logo_img
    sidebar_logo_img = None
    try:
        script_dir = os.path.dirname(__file__)
        logo_path_attempt = os.path.join(script_dir, "testlogo.png")
        if not os.path.exists(logo_path_attempt):
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
            print("Warning: testlogo.png not found in dashboard directory. Using placeholder text.")
    except Exception as e:
        print(f"Error loading sidebar logo: {e}. Using placeholder text.")
        logo_label = tk.Label(sidebar_frame, text="TrackU Logo", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR,
                              fg="darkgray")
        logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")

    menu_items = ["", "", "Dashboard", "Total Expenses", "Total Savings", "", "", "", "", "", "Profile"]
    sidebar_frame.grid_rowconfigure(len(menu_items) * 2 + 1, weight=1)

    row_idx = 1
    for item in menu_items:
        if item:
            menu_button = tk.Button(
                sidebar_frame,
                text=item,
                font=FONT_MENU,
                bg=COLOR_SIDEBAR,
                fg="black",
                command=lambda i=item: on_menu_item_click(i, root_window),
                relief="flat",
                activebackground=COLOR_NAVBAR,
                anchor="w",
                padx=15
            )
            if item == "Total Expenses":
                menu_button.config(bg=COLOR_NAVBAR)

            def _on_enter(event, btn=menu_button, current=item, current_page="Total Expenses"):
                if current != current_page:
                    btn.config(bg="#e0e0e0")

            def _on_leave(event, btn=menu_button, current=item, current_page="Total Expenses"):
                if current != current_page:
                    btn.config(bg=COLOR_SIDEBAR)

            menu_button.bind("<Enter>", _on_enter)
            menu_button.bind("<Leave>", _on_leave)

            menu_button.grid(row=row_idx, column=0, pady=5, sticky="ew")
            row_idx += 1

            if item != menu_items[-1] and item != "":
                tk.Frame(sidebar_frame, bg=COLOR_BOX_BORDER, height=1).grid(row=row_idx, column=0, sticky="ew", padx=10)
                row_idx += 1
        else:
            tk.Label(sidebar_frame, text="", bg=COLOR_SIDEBAR).grid(row=row_idx, column=0, pady=10)
            row_idx += 1

    sidebar_frame.grid_rowconfigure(row_idx, weight=1)

    # --- Top Right Header Canvas ---
    top_right_header_canvas = tk.Canvas(root_window, bg=COLOR_BG, height=85, highlightthickness=0)
    top_right_header_canvas.grid(row=0, column=1, sticky="nsew")
    top_right_header_canvas.bind("<Configure>", draw_top_right_header_content)

    # --- Main Content Area ---
    main_content_area = tk.Frame(root_window, bg=COLOR_BG)
    main_content_area.grid(row=1, column=1, sticky="nsew", padx=30, pady=20)
    main_content_area.grid_columnconfigure(0, weight=1, minsize=300)
    main_content_area.grid_columnconfigure(1, weight=1)
    main_content_area.grid_rowconfigure(0, weight=1)

    # --- Pie Chart Section ---
    pie_chart_section_canvas = tk.Canvas(main_content_area, bg=COLOR_BG, highlightthickness=0)
    pie_chart_section_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=10)

    # Month combobox for pie chart - CREATED ONCE HERE
    months = [calendar.month_name[i] for i in range(1, 13)]
    month_combo_widget_ref = ttk.Combobox(pie_chart_section_canvas, textvariable=month_var, values=months,
                                          state="readonly", font=FONT_SUBTEXT, justify="center", width=15)
    month_combo_widget_ref.current(datetime.now().month - 1)
    month_combo_widget_ref.bind("<<ComboboxSelected>>", lambda e: refresh_data_and_ui())

    # Total expenses amount label - CREATED ONCE HERE
    total_expenses_amount_lbl_widget_ref = tk.Label(pie_chart_section_canvas, text="Total Expenses:\n₱ 0.00",
                                                    font=("Georgia", 13), bg=COLOR_BG, fg="black", justify=tk.LEFT)

    pie_chart_section_canvas.bind("<Configure>", update_pie_chart_section)


    # --- Recent Transaction Box ---
    recent_transaction_canvas = tk.Canvas(main_content_area, bg=COLOR_BG, highlightthickness=0)
    recent_transaction_canvas.grid(row=0, column=1, sticky="nsew", pady=10)

    # Add button - CREATED ONCE HERE
    add_transaction_button = tk.Button(
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
    # Get initial width for placement
    root_window.update_idletasks() # Ensure widgets are measured
    initial_canvas_width = recent_transaction_canvas.winfo_width()
    add_transaction_button_window_id = recent_transaction_canvas.create_window(
        initial_canvas_width - 30, 20, window=add_transaction_button, anchor="ne"
    )

    # Category Combobox for Recent Transactions - CREATED ONCE HERE
    # Removed the redundant `global recent_transaction_category_combobox_var` from here
    # as it's already declared global at the module level and in the function header.
    if recent_transaction_category_combobox_var is None: # This check is still valid
        recent_transaction_category_combobox_var = tk.StringVar(value="All Categories")

    categories_from_db = sorted(list(set(item[0] for item in database_manager.get_all_expenses())))
    categories_for_filter = ["All Categories"] + categories_from_db

    recent_transaction_category_combobox = ttk.Combobox(
        recent_transaction_canvas,
        textvariable=recent_transaction_category_combobox_var,
        values=categories_for_filter,
        state="readonly",
        width=15,
        font=FONT_SUBTEXT,
        justify="center",
    )
    if recent_transaction_category_combobox_var.get() not in categories_for_filter:
        recent_transaction_category_combobox_var.set("All Categories")
    recent_transaction_category_combobox.bind("<<ComboboxSelected>>", lambda e: refresh_data_and_ui())
    recent_transaction_category_combobox_window_id = recent_transaction_canvas.create_window(
        30, 60, window=recent_transaction_category_combobox, anchor="nw"
    )


    recent_transaction_canvas.bind("<Configure>", update_recent_transaction_box)

    root_window.update_idletasks()
    refresh_data_and_ui() # Initial draw


    root_window.mainloop()


if __name__ == "__main__":
    create_total_expenses_app()