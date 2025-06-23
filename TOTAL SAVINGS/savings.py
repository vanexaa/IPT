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

# --- Path setup for database_manager.py ---
# Get the directory of the current script (NewTrials.py is in TOTAL SAVINGS/)
current_script_dir = os.path.dirname(__file__)

# Go up one level (from TOTAL SAVINGS/ to Python Coding/)
# Then go down into 'TOTAL EXPENSES' where database_manager.py is
database_folder_path = os.path.abspath(os.path.join(current_script_dir, "..", "TOTAL EXPENSES"))

# Add this path to sys.path
if database_folder_path not in sys.path:
    sys.path.append(database_folder_path)
# ------------------------------------------


import database_manager

try:
    pyglet.font.add_file('Playfair Display.ttf')
except Exception as e:
    print(f"Warning: Could not load Playfair Display.ttf. Using default system fonts. Error: {e}")

# --- Colors ---
COLOR_BG = "#fdfdf5"
COLOR_NAVBAR = "#ffe0b2"
COLOR_SIDEBAR = "#d6e9d5"
COLOR_CANVAS_BAR = "#fdf6e3"
COLOR_PIE_SLICE_1 = "#4dd0e1"  # Teal for Savings
COLOR_PIE_SLICE_2 = "#ff8a65"  # Orange for Savings
COLOR_PIE_SLICE_3 = "#ffd54f"  # Yellow for Savings
COLOR_PIE_SLICE_4 = "#aed581"  # Green
COLOR_PIE_SLICE_5 = "#b39ddb"  # Purple
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
total_savings_header_label_tk = None
canvas_chart_widget_ref = None  # Keep this global for managing Matplotlib canvas

# --- Global Tkinter StringVars for comboboxes (crucial for persistence) ---
month_var = None
recent_transaction_category_combobox_var = None
# -------------------------------------------------------------------------

# --- NEW Global References for Tkinter Widgets for persistence ---
# These will now hold the actual Tkinter widget instances.
# Declared here to be accessible throughout the module.
month_combo_widget_ref = None
total_savings_amount_lbl_widget_ref = None
recent_transaction_category_combobox = None
recent_transaction_category_combobox_window_id = None
add_button_ref = None  # Global reference for the "Add" button
add_button_window_id = None # Global reference for the window item ID of the add button
# -----------------------------------------------------------------

# Global variables to store current month/year for filtering
current_display_month_num = datetime.now().month
current_display_year = datetime.now().year

# Global reference to the main Tkinter root window
root_window = None


def on_menu_item_click(item_name, current_root):
    """Handles the click event for sidebar menu items."""
    script_dir = os.path.dirname(__file__)
    script_to_launch = None
    if item_name == "Dashboard":
        script_to_launch = os.path.join(script_dir, "..", "DASHBOARD", "dashboard.py")
    elif item_name == "Total Expenses":
        # Adjust path to expenses.py if it's not in the same folder as NewTrials.py
        script_to_launch = os.path.join(script_dir, "..", "TOTAL EXPENSES", "expenses.py")
    elif item_name == "Total Savings":
        print("Already on Total Savings page!")
        return
    elif item_name == "Profile":
        print("Profile clicked!")
        return

    if script_to_launch:
        try:
            subprocess.Popen([sys.executable, script_to_launch])
            if item_name != "Total Savings":
                current_root.destroy()
        except Exception as e:
            print(f"Failed to launch {script_to_launch}: {e}")


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


def on_add_button_click():
    """Launches the Savings-Categories.py script in a new window."""
    script_dir = os.path.dirname(__file__)
    # Point to the dedicated Savings-Categories.py file
    script_to_launch = os.path.join(script_dir, "Saving-Categories.py")

    if os.path.exists(script_to_launch):
        try:
            subprocess.Popen([sys.executable, script_to_launch])
            print(f"Launched {script_to_launch}")
            # Schedule a refresh for this window after a short delay, hoping the child window has closed
            root_window.after(500, refresh_data_and_ui)
        except Exception as e:
            print(f"Failed to launch {script_to_launch}: {e}")
    else:
        print(f"Error: {script_to_launch} not found. Please create this file.")


def refresh_data_and_ui():
    """
    Function to call when data needs to be refreshed (e.g., after adding a transaction
    or changing a filter). This will trigger a re-draw of the pie chart and recent transactions.
    """
    # Directly call the update functions, which will now use global widget references
    update_pie_chart_section() # No event needed as it pulls dimensions from global canvas
    update_recent_transaction_box() # No event needed as it pulls dimensions from global canvas


def update_pie_chart_section(event=None): # Make event optional
    """
    Updates the content of the left-side section (month, pie chart, savings details).
    Uses global widget references for month combobox and total savings label.
    """
    global canvas_chart_widget_ref, current_display_month_num, current_display_year
    global month_combo_widget_ref, total_savings_amount_lbl_widget_ref # Access global refs here

    # Ensure canvases and widgets exist before proceeding
    if not pie_chart_section_canvas or not month_combo_widget_ref or not total_savings_amount_lbl_widget_ref:
        return

    pie_chart_section_canvas.delete("all")  # Clear the canvas, but will redraw persistent widgets

    # Get current dimensions from the canvas, or use a default if event is None
    if event:
        current_width = event.width
        current_height = event.height
    else:
        current_width = pie_chart_section_canvas.winfo_width()
        current_height = pie_chart_section_canvas.winfo_height()
        if current_width == 1 or current_height == 1: # Avoid issues with minimal widget size during initialization
             return # Wait for proper sizing if not already set

    # Peso sign watermark for the pie chart section - Draw first, then lower
    pie_chart_section_canvas.create_text(current_width / 2, current_height / 2, text="₱",
                       font=("Arial", int(current_height * 0.7), "bold"),
                       fill="#f0f0e0", anchor="center", tags="pie_watermark")
    pie_chart_section_canvas.tag_lower("pie_watermark")

    # Position month combobox (centered horizontally at the top)
    # Get selected month name, convert to number
    selected_month_name = month_combo_widget_ref.get() # Use the global ref
    try:
        month_to_num = {name: i for i, name in enumerate(calendar.month_name) if i > 0}
        current_display_month_num = month_to_num.get(selected_month_name, datetime.now().month)
    except ValueError:
        current_display_month_num = datetime.now().month

    current_display_year = datetime.now().year

    # Re-place the month combobox on the canvas (it might have been deleted by canvas.delete("all"))
    pie_chart_section_canvas.create_window(current_width / 2, 40, window=month_combo_widget_ref, anchor="n")

    # --- Fetch data from database for Pie Chart ---
    savings_breakdown = database_manager.get_savings_breakdown_by_month_year(current_display_month_num,
                                                                             current_display_year)
    total_savings_for_month = database_manager.get_total_savings_by_month_year(current_display_month_num,
                                                                               current_display_year)

    # Matplotlib Pie Chart setup
    chart_height_ratio = 0.6
    fig, ax = plt.subplots(figsize=(current_width / 100, (current_height * chart_height_ratio) / 100), dpi=100,
                           facecolor=COLOR_BG)

    # --- Handle cases with no savings or zero total savings ---
    if not savings_breakdown or total_savings_for_month <= 0:
        labels = ["No Savings"]
        sizes = [1]
        center_text = f"No Savings This Month\n(for {selected_month_name} {current_display_year})"
        total_savings_for_month = 0.0

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
        labels = [item[0] for item in savings_breakdown]
        sizes = [item[1] for item in savings_breakdown]

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

        center_text = f"Savings Breakdown\nTotal: ₱{total_savings_for_month:,.2f}"

        ax.text(0, 0, center_text, horizontalalignment='center', verticalalignment='center',
                fontsize=FONT_SECTION[1], color='gray', transform=ax.transAxes)

    if canvas_chart_widget_ref:
        canvas_chart_widget_ref.destroy()

    canvas_chart_agg = FigureCanvasTkAgg(fig, master=pie_chart_section_canvas)
    canvas_chart_widget = canvas_chart_agg.get_tk_widget()
    canvas_chart_widget.config(bg=COLOR_BG)
    chart_center_y = current_height * (0.15 + chart_height_ratio / 2)
    pie_chart_section_canvas.create_window(current_width / 2, chart_center_y, window=canvas_chart_widget, anchor="center")
    canvas_chart_widget_ref = canvas_chart_widget

    # Update total savings label
    total_savings_amount_lbl_widget_ref.config(text=f"Total Savings:\n₱ {total_savings_for_month:,.2f}") # Use global ref
    total_savings_y = current_height * (0.15 + chart_height_ratio) + 30
    pie_chart_section_canvas.create_window(current_width / 2, total_savings_y, window=total_savings_amount_lbl_widget_ref, anchor="n")

    plt.close(fig)


def update_recent_transaction_box(event=None): # Make event optional
    """
    Updates the content of the right-side recent transactions box on resize.
    Now ensures the combobox and add button persist by not deleting them.
    """
    global recent_transaction_category_combobox, recent_transaction_category_combobox_window_id, add_button_ref, add_button_window_id, recent_transaction_category_combobox_var

    if not recent_transaction_canvas:
        return

    # !!! CRITICAL CHANGE: Only delete specific items, not "all" !!!
    # Delete previous transaction list items, watermark, and static text if they are being redrawn.
    recent_transaction_canvas.delete("transaction_item")
    recent_transaction_canvas.delete("watermark")
    recent_transaction_canvas.delete("static_text") # Tag for titles and headers

    # Get current dimensions from the canvas, or use a default if event is None
    if event:
        current_width = event.width
        current_height = event.height
    else:
        current_width = recent_transaction_canvas.winfo_width()
        current_height = recent_transaction_canvas.winfo_height()
        if current_width == 1 or current_height == 1:
            return

    # 1. Draw the main rounded rectangle background
    draw_rounded_rect(recent_transaction_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR,
                      outline_width=0)

    # 2. Draw the peso sign watermark.
    recent_transaction_canvas.create_text(current_width / 2, current_height / 2, text="₱",
                                          font=("Arial", int(current_height * 0.7), "bold"),
                                          fill="#f0f0e0", anchor="center", tags="watermark")
    recent_transaction_canvas.tag_lower("watermark")

    # 3. Draw other static foreground content (titles/headers) using tags for selective deletion
    recent_transaction_canvas.create_text(20, 20, anchor="nw", text="Recent Savings", font=FONT_SECTION,
                                          fill="black", tags="static_text") # Tagged
    recent_transaction_canvas.create_text(current_width - 30, 60, anchor="ne", text="Amount", font=FONT_SUBTEXT,
                                          fill="black", tags="static_text") # Tagged


    # Add Button (text-based) - ENSURE POSITION IS UPDATED
    # The button is created once in create_total_savings_app, so just update its position
    recent_transaction_canvas.coords(add_button_window_id, current_width - 30, 20)
    recent_transaction_canvas.tag_raise(add_button_window_id)


    # --- Category Dropdown --- ENSURE POSITION AND VALUES ARE UPDATED
    # The combobox is created once in create_total_savings_app.
    # Update values in combobox in case new categories were added
    categories_from_db = sorted(
        list(set(item[1] for item in database_manager.get_all_savings())))
    categories_for_filter = ["All Categories"] + categories_from_db

    recent_transaction_category_combobox['values'] = categories_for_filter
    # Ensure the current selection is still valid after updating values
    if recent_transaction_category_combobox_var.get() not in categories_for_filter:
        recent_transaction_category_combobox_var.set("All Categories")

    # Update combobox position
    recent_transaction_canvas.coords(recent_transaction_category_combobox_window_id, 20, 60)
    recent_transaction_canvas.tag_raise(recent_transaction_category_combobox_window_id)


    # --- Fetch recent savings from database and apply filter ---
    selected_filter_category = recent_transaction_category_combobox_var.get()
    all_savings = database_manager.get_all_savings()

    if selected_filter_category != "All Categories":
        filtered_savings = [s for s in all_savings if s[1] == selected_filter_category]
    else:
        filtered_savings = all_savings

    y_offset = 90
    line_height = 28
    display_limit = int((current_height - y_offset - 30) / line_height)

    # Display "No Recent Savings" if list is empty
    if not filtered_savings:
        recent_transaction_canvas.create_text(
            current_width / 2, y_offset + line_height,
            anchor="center",
            text="No Recent Savings",
            font=FONT_SUBTEXT,
            fill="gray",
            tags="transaction_item" # Tagged for selective deletion
        )
    else:
        for idx, (id, category, amount, transaction_date_str, notes) in enumerate(filtered_savings):
            if idx >= display_limit:
                break

            display_amount = f"₱{amount:,.2f}"
            if amount >= 0:
                display_amount = f"+{display_amount}"

            try:
                dt_obj = datetime.strptime(transaction_date_str, "%Y-%m-%d %H:%M:%S")
                display_date = dt_obj.strftime("%b %d, %Y")
            except ValueError:
                display_date = "Invalid Date"

            display_text = f"• {category} ({display_date})"

            recent_transaction_canvas.create_text(30, y_offset, anchor="w", text=display_text, font=FONT_TRANSACTION,
                                                  fill="black", tags="transaction_item") # Tagged
            recent_transaction_canvas.create_text(current_width - 30, y_offset, anchor="e", text=display_amount,
                                                  font=FONT_TRANSACTION, fill="black", tags="transaction_item") # Tagged
            y_offset += line_height


def create_total_savings_app():
    global root_window, month_var, recent_transaction_category_combobox_var
    global pie_chart_section_canvas, recent_transaction_canvas, top_right_header_canvas
    global month_combo_widget_ref, total_savings_amount_lbl_widget_ref
    global recent_transaction_category_combobox, recent_transaction_category_combobox_window_id, add_button_ref, add_button_window_id

    root_window = tk.Tk()
    root_window.title("TrackU - Total Savings")
    root_window.state("zoomed")
    root_window.configure(bg=COLOR_BG)

    database_manager.initialize_db()

    root_window.grid_columnconfigure(0, weight=0, minsize=250)
    root_window.grid_columnconfigure(1, weight=1)
    root_window.grid_rowconfigure(0, weight=0, minsize=85)
    root_window.grid_rowconfigure(1, weight=1)

    # --- Initialize global StringVars BEFORE widgets are created ---
    month_var = tk.StringVar(value=calendar.month_name[datetime.now().month])
    recent_transaction_category_combobox_var = tk.StringVar(value="All Categories")
    # ---------------------------------------------------------------

    # --- LEFT SIDEBAR FRAME ---
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
            if row_idx > 1 and menu_items[menu_items.index(item) - 1] != "" and item != "Dashboard":
                separator_frame = tk.Frame(sidebar_frame, bg=COLOR_BOX_BORDER, height=1)
                separator_frame.grid(row=row_idx, column=0, sticky="ew", padx=10, pady=(5, 5))
                row_idx += 1

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
            if item == "Total Savings":
                menu_button.config(bg=COLOR_NAVBAR)

            def _on_enter(event, btn=menu_button, current=item, current_page="Total Savings"):
                if current != current_page:
                    btn.config(bg="#e0e0e0")

            def _on_leave(event, btn=menu_button, current=item, current_page="Total Savings"):
                if current != current_page:
                    btn.config(bg=COLOR_SIDEBAR)

            menu_button.bind("<Enter>", _on_enter)
            menu_button.bind("<Leave>", _on_leave)

            menu_button.grid(row=row_idx, column=0, pady=5, sticky="ew")
            row_idx += 1
        else:
            if item == "" and "Profile" in menu_items and menu_items.index("Profile") == menu_items.index(item) + 1:
                sidebar_frame.grid_rowconfigure(row_idx, weight=1)
            tk.Label(sidebar_frame, text="", bg=COLOR_SIDEBAR).grid(row=row_idx, column=0, pady=0)
            row_idx += 1

    sidebar_frame.grid_rowconfigure(row_idx, weight=1)

    # --- TOP RIGHT HEADER / NAVBAR ---
    top_right_header_canvas = tk.Canvas(root_window, bg=COLOR_BG, height=85, highlightthickness=0)
    top_right_header_canvas.grid(row=0, column=1, sticky="nsew")
    top_right_header_canvas.bind("<Configure>", draw_top_right_header_content)

    # --- MAIN CONTENT FRAME ---
    main_content_area = tk.Frame(root_window, bg=COLOR_BG)
    main_content_area.grid(row=1, column=1, sticky="nsew", padx=30, pady=20)
    main_content_area.grid_columnconfigure(0, weight=1, minsize=300)
    main_content_area.grid_columnconfigure(1, weight=1)
    main_content_area.grid_rowconfigure(0, weight=1)

    # --- LEFT SECTION: Pie Chart and Savings Details ---
    pie_chart_section_canvas = tk.Canvas(main_content_area, bg=COLOR_BG, highlightthickness=0)
    pie_chart_section_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=10)

    # Month combobox for pie chart - CREATED ONCE HERE
    months = [calendar.month_name[i] for i in range(1, 13)]
    month_combo_widget_ref = ttk.Combobox(pie_chart_section_canvas, textvariable=month_var, values=months,
                               state="readonly", font=FONT_SUBTEXT, justify="center", width=15)
    month_combo_widget_ref.current(datetime.now().month - 1)
    month_combo_widget_ref.bind("<<ComboboxSelected>>", lambda e: refresh_data_and_ui())

    # Total savings amount label - CREATED ONCE HERE
    total_savings_amount_lbl_widget_ref = tk.Label(pie_chart_section_canvas, text="Total Savings:\n₱ 0.00",
                                        font=("Georgia", 13), bg=COLOR_BG, fg="black", justify=tk.LEFT)

    pie_chart_section_canvas.bind("<Configure>", update_pie_chart_section) # Bind to general update

    # --- RIGHT SECTION: Recent Savings ---
    recent_transaction_canvas = tk.Canvas(main_content_area, bg=COLOR_BG, highlightthickness=0)
    recent_transaction_canvas.grid(row=0, column=1, sticky="nsew", pady=10)

    # Add button - CREATED ONCE HERE
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
    root_window.update_idletasks() # Ensure sizes are calculated before initial placement
    initial_canvas_width = recent_transaction_canvas.winfo_width()
    add_button_window_id = recent_transaction_canvas.create_window(
        initial_canvas_width - 30, 20, window=add_button_ref, anchor="ne"
    )

    # Category Combobox for Recent Transactions - CREATED ONCE HERE
    categories_from_db = sorted(list(set(item[1] for item in database_manager.get_all_savings())))
    categories_for_filter = ["All Categories"] + categories_from_db
    recent_transaction_category_combobox = ttk.Combobox(
        recent_transaction_canvas,
        textvariable=recent_transaction_category_combobox_var, # Use global StringVar
        values=categories_for_filter,
        state="readonly",
        width=15,
        font=FONT_SUBTEXT,
        justify="center"
    )
    if recent_transaction_category_combobox_var.get() not in categories_for_filter:
        recent_transaction_category_combobox_var.set("All Categories")
    recent_transaction_category_combobox.bind("<<ComboboxSelected>>", lambda e: refresh_data_and_ui())
    recent_transaction_category_combobox_window_id = recent_transaction_canvas.create_window(
        20, 60, window=recent_transaction_category_combobox, anchor="nw"
    )

    recent_transaction_canvas.bind("<Configure>", update_recent_transaction_box)

    # Initial call to populate data after all widgets are set up
    root_window.update_idletasks() # Ensure sizes are calculated before initial draw
    refresh_data_and_ui()


    root_window.mainloop()


if __name__ == "__main__":
    create_total_savings_app()
