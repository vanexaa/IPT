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
import tkinter.messagebox as messagebox  # Import messagebox for error pop-ups

# --- Path setup for database_manager.py ---
# Get the directory of the current script (savings.py is in TOTAL SAVINGS/)
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
FONT_MENU = ("Playfair Display", 13)  # Increased font size for menu items
FONT_SECTION = ("Georgia", 16, "bold")
FONT_SUBTEXT = ("Playfair Display", 12)
FONT_TRANSACTION = ("Playfair Display", 11)
FONT_WELCOME = ("Playfair Display", 22, "bold")  # Added for welcome message

LOGO_SIZE_SIDEBAR = (150, 100)
ICON_SIZE = (60, 60)  # Increased icon size to fit larger boxes

# --- Global constant for Sidebar Width ---
SIDEBAR_WIDTH = 400

# Global dictionary to store PhotoImage objects for sidebar icons
sidebar_icons = {}

# Global references for labels in the header to prevent garbage collection
tracku_label_tk = None
total_savings_header_label_tk = None
canvas_chart_widget_ref = None  # Keep this global for managing Matplotlib canvas

# --- Global Tkinter StringVars for comboboxs (crucial for persistence) ---
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
add_button_window_id = None  # Global reference for the window item ID of the add button

# Header labels and their canvas IDs
tracku_label_tk_id = None
total_savings_header_label_tk_id = None

# Canvases need to be global too for easier access in update functions
pie_chart_section_canvas = None
recent_transaction_canvas = None
top_right_header_canvas = None
# -----------------------------------------------------------------

# Global variables to store current month/year for filtering
current_display_month_num = datetime.now().month
current_display_year = datetime.now().year

# --- Global reference to the main Tkinter root window ---
root_window = None

# --- Global variable to store the logged-in user's ID and Username ---
logged_in_user_id = None
logged_in_username = "Guest"  # Default value if no user is passed

# Reference for welcome label in main content area
welcome_label_ref = None

# Global reference for child process launched by category click
category_child_process_ref = None


def on_menu_item_click(item_name, current_root):
    """Handles the click event for sidebar menu items."""
    script_dir = os.path.dirname(__file__)
    script_to_launch = None

    global logged_in_user_id  # Access global user ID

    if item_name == "Dashboard":
        script_to_launch = os.path.join(script_dir, "..", "DASHBOARD", "dashboard.py")
    elif item_name == "Total Expenses":
        # Adjust path to expenses.py if it's not in the same folder as NewTrials.py
        script_to_launch = os.path.join(script_dir, "..", "TOTAL EXPENSES", "expenses.py")
    elif item_name == "Total Savings":
        print("Already on Total Savings page!")
        return
    elif item_name == "Profile":
        script_to_launch = os.path.join(script_dir, "profile.py")

    if script_to_launch:
        try:
            # Only destroy the main window if NOT opening Profile
            if item_name != "Profile":
                if root_window and root_window.winfo_exists():
                    root_window.destroy()

            cmd = [sys.executable, script_to_launch]
            if logged_in_user_id is not None:
                cmd.append(str(logged_in_user_id))

            if sys.platform.startswith('win'):
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen(cmd)
            print(f"Launched: {script_to_launch}")
        except FileNotFoundError:
            messagebox.showerror("Launch Error", f"Script not found: {script_to_launch}. Ensure paths are correct.")
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch {script_to_launch}:\n{e}")
            print(f"Launched: {script_to_launch}")

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
    global tracku_label_tk, total_savings_header_label_tk, tracku_label_tk_id, total_savings_header_label_tk_id
    global logged_in_username  # Access logged_in_username

    top_right_header_canvas.delete("all")
    draw_bottom_rounded_rect(top_right_header_canvas, 0, 0, event.width, event.height, 20, COLOR_NAVBAR)

    # Recreate or reposition labels
    if tracku_label_tk is None:
        tracku_label_tk = tk.Label(top_right_header_canvas, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
    if total_savings_header_label_tk is None:
        total_savings_header_label_tk = tk.Label(top_right_header_canvas, text="Total Savings", font=("Georgia", 16),
                                                 bg=COLOR_NAVBAR, fg="#222")

    # If IDs exist, just re-position. Otherwise, create new window items.
    if tracku_label_tk_id:
        top_right_header_canvas.coords(tracku_label_tk_id, 30, event.height / 2)
    else:
        tracku_label_tk_id = top_right_header_canvas.create_window(30, event.height / 2, window=tracku_label_tk,
                                                                   anchor="w")

    # MODIFIED: Display logged-in username in the top right header
    if logged_in_username and logged_in_username != "Guest":
        header_text = f"Total Savings"
    else:
        header_text = "Total Savings"

    total_savings_header_label_tk.config(text=header_text)

    if total_savings_header_label_tk_id:
        top_right_header_canvas.coords(total_savings_header_label_tk_id, event.width - 30, event.height / 2)
    else:
        total_savings_header_label_tk_id = top_right_header_canvas.create_window(event.width - 30, event.height / 2,
                                                                                 window=total_savings_header_label_tk,
                                                                                 anchor="e")

    # Ensure labels are on top
    top_right_header_canvas.tag_raise(tracku_label_tk_id)
    top_right_header_canvas.tag_raise(total_savings_header_label_tk_id)


def on_add_button_click():
    """Launches the Saving-Categories.py script and refreshes UI after it closes."""
    global logged_in_user_id  # Access global user ID
    script_dir = os.path.dirname(__file__)
    script_to_launch = os.path.join(script_dir, "Saving-Categories.py")

    if os.path.exists(script_to_launch):
        try:
            cmd = [sys.executable, script_to_launch]
            if logged_in_user_id is not None:
                cmd.append(str(logged_in_user_id))  # Pass the user ID

            proc = subprocess.Popen(cmd)
            print(f"Launched {script_to_launch} for user ID {logged_in_user_id}")

            def poll_popup():
                if proc.poll() is None:
                    root_window.after(300, poll_popup)
                else:
                    refresh_data_and_ui()

            poll_popup()
        except FileNotFoundError:
            messagebox.showerror("Launch Error", f"Script not found: {script_to_launch}. Ensure paths are correct.")
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch {script_to_launch}:\n{e}")


def refresh_data_and_ui():
    """
    Function to call when data needs to be refreshed (e.g., after adding a transaction
    or changing a filter). This will trigger a re-draw of the pie chart and recent transactions.
    """
    # Directly call the update functions, which will now use global widget references
    update_pie_chart_section()  # No event needed as it pulls dimensions from global canvas
    update_recent_transaction_box()  # No event needed as it pulls dimensions from global canvas


# This function was incorrectly placed inside update_pie_chart_section in the original code.
# It is moved to the global scope as it is intended to be a standalone event handler.
def check_category_child_process_status():
    """
    Periodically checks if the launched category child process has exited.
    If it has, triggers a UI refresh.
    """
    global category_child_process_ref
    if category_child_process_ref and category_child_process_ref.poll() is None:
        # Process is still running, check again soon
        root_window.after(100, check_category_child_process_status)
    elif category_child_process_ref and category_child_process_ref.poll() is not None:
        # Process has exited, refresh UI
        print("Category child process exited. Refreshing UI.")
        refresh_data_and_ui()
        category_child_process_ref = None  # Clear reference
    else:
        # No child process launched or already handled
        pass


# This function was incorrectly placed inside update_pie_chart_section in the original code.
# It is moved to the global scope as it is intended to be a standalone event handler.
def on_recent_transaction_canvas_click(event):
    global recent_transaction_category_combobox_var, logged_in_user_id, category_child_process_ref

    items_at_click = recent_transaction_canvas.find_overlapping(event.x - 2, event.y - 2, event.x + 2, event.y + 2)

    for item_id in items_at_click:
        tags = recent_transaction_canvas.gettags(item_id)
        if "category_link" in tags:
            clicked_category_text = recent_transaction_canvas.itemcget(item_id, "text")
            script_dir = os.path.dirname(__file__)
            script_to_launch = os.path.join(script_dir, "Edit-Savings.py")

            if os.path.exists(script_to_launch):
                try:
                    cmd = [sys.executable, script_to_launch]
                    if logged_in_user_id is not None:
                        cmd.append(str(logged_in_user_id))
                    cmd.append(clicked_category_text)

                    category_child_process_ref = subprocess.Popen(cmd)

                    def poll_popup():
                        global category_child_process_ref
                        if category_child_process_ref is not None and category_child_process_ref.poll() is None:
                            root_window.after(300, poll_popup)
                        else:
                            refresh_data_and_ui()
                            category_child_process_ref = None

                    poll_popup()
                except Exception as e:
                    messagebox.showerror("Launch Error", f"Failed to launch {script_to_launch}:\n{e}")
            return

def update_pie_chart_section(event=None):  # Make event optional
    """
    Updates the content of the left-side section (month, pie chart, savings details).
    Uses global widget references for month combobox and total savings label.
    """
    global canvas_chart_widget_ref, current_display_month_num, current_display_year
    global month_combo_widget_ref, total_savings_amount_lbl_widget_ref  # Access global refs here
    global logged_in_user_id  # Ensure user_id is accessible for database calls

    # Ensure canvases and widgets exist before proceeding
    if not pie_chart_section_canvas or month_combo_widget_ref is None or total_savings_amount_lbl_widget_ref is None:
        return

    # Clear old chart.
    if canvas_chart_widget_ref:
        canvas_chart_widget_ref.destroy()  # Destroy the old Matplotlib Tkinter widget
        canvas_chart_widget_ref = None  # Clear reference
    pie_chart_section_canvas.delete("pie_watermark")  # delete only pie chart specific watermark

    # Get current dimensions from the canvas, or use a default if event is None
    # Wait for the canvas to be mapped to get reliable dimensions
    if event:  # If called by configure event, use event.width/height
        current_width = event.width
        current_height = event.height
    else:  # If called manually, force update and get dimensions
        pie_chart_section_canvas.update_idletasks()
        current_width = pie_chart_section_canvas.winfo_width()
        current_height = pie_chart_section_canvas.winfo_height()

    if current_width <= 1 or current_height <= 1:  # Avoid issues with minimal widget size during initialization
        return  # Wait for proper sizing if not already set

    # Reposition and raise the month combobox using its canvas ID
    pie_chart_section_canvas.delete("month_combo")  # Remove old one if exists before recreating
    pie_chart_section_canvas.create_window(current_width / 2, 40, window=month_combo_widget_ref, anchor="n",
                                           tags="month_combo")
    pie_chart_section_canvas.tag_raise("month_combo")  # Ensure it's on top

    # Peso sign watermark for the pie chart section - Draw first, then lower
    pie_chart_section_canvas.create_text(current_width / 2, current_height / 2, text="₱",
                                         font=("Arial", int(current_height * 0.7 * 0.5), "bold"),  # Adjusted font size
                                         fill="#f0f0f0", anchor="center", tags="pie_watermark")
    pie_chart_section_canvas.tag_lower("pie_watermark")

    # Get selected month name, convert to number
    selected_month_name = month_combo_widget_ref.get()  # Use the global ref
    try:
        month_to_num = {name: i for i, name in enumerate(calendar.month_name) if i > 0}
        current_display_month_num = month_to_num.get(selected_month_name, datetime.now().month)
    except ValueError:
        current_display_month_num = datetime.now().month

    current_display_year = datetime.now().year

    # --- Fetch data from database for Pie Chart ---
    # MODIFIED: If savings are tied to user_id, you'd need to modify database_manager.py
    # and pass user_id to these functions:
    # savings_breakdown = database_manager.get_savings_breakdown_by_month_year(logged_in_user_id, current_display_month_num, current_display_year)
    # total_savings_for_month = database_manager.get_total_savings_by_month_year(logged_in_user_id, current_display_month_num, current_display_year)
    savings_breakdown = database_manager.get_savings_breakdown_by_month_year(current_display_month_num,
                                                                             current_display_year)
    total_savings_for_month = database_manager.get_total_savings_by_month_year(current_display_month_num,
                                                                               current_display_year)

    # Calculate available space for the chart
    chart_top_y = 40 + 20  # Below month combobox + some margin
    chart_bottom_y = current_height - 30 - 20  # Keep margin at bottom, adjusted to make space for legend
    chart_display_height = chart_bottom_y - chart_top_y

    if chart_display_height <= 0 or current_width <= 0:
        print("Warning: Insufficient space for pie chart.")
        return

    # Calculate figsize in inches, aiming for a square chart within available space
    chart_effective_width_px = current_width * 0.9  # Give 10% horizontal padding
    chart_effective_height_px = chart_display_height * 0.9  # Give 10% vertical padding

    # Made graph smaller by adjusting scaling factor to 0.75 as per user request
    chart_size_px = min(chart_effective_width_px, chart_effective_height_px) * 0.80
    chart_size_inches = chart_size_px / 100.0  # Convert pixels to inches for matplotlib figsize

    fig, ax = plt.subplots(figsize=(chart_size_inches, chart_size_inches), dpi=100,
                           facecolor='none')  # Made figure background invisible
    ax.set_facecolor('none')  # Made axes background invisible
    ax.axis('equal')  # Ensure pie is circular

    # --- Handle cases with no savings or zero total savings ---
    if not savings_breakdown or total_savings_for_month <= 0:
        labels = ["No Savings"]
        sizes = [1]
        center_text = f"No Savings This Month\n(for {selected_month_name} {current_display_year})"

        ax.text(0.5, 0.5, center_text,
                horizontalalignment='center', verticalalignment='center',
                fontsize=FONT_SECTION[1], color='gray', transform=ax.transAxes, wrap=True)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        total_savings_for_month = 0.0  # Ensure total is 0 if no data
        wedges = []  # Set wedges to empty for no data case
        autotexts = []
    else:
        labels = [item[0] for item in savings_breakdown]
        sizes = [item[1] for item in savings_breakdown]

        pie_colors = [COLOR_PIE_SLICE_1, COLOR_PIE_SLICE_2, COLOR_PIE_SLICE_3, COLOR_PIE_SLICE_4, COLOR_PIE_SLICE_5,
                      "#cccccc", "#ffcc00", "#99ff99"]
        actual_colors = [pie_colors[i % len(pie_colors)] for i in range(len(sizes))]

        # Removed explode parameter and adjusted wedgeprops for a solid circle
        wedges, texts, autotexts = ax.pie(sizes, colors=actual_colors, startangle=140,
                                          wedgeprops=dict(width=1.0), autopct='%1.1f%%',
                                          pctdistance=0.85)

        for text in texts:
            text.set_color('black')
            text.set_fontsize(FONT_SUBTEXT[1])

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(FONT_SUBTEXT[1] - 2)

        # Removed center text with total amount from the pie chart as per user request
        # ax.text(0, 0, center_text, horizontalalignment='center', verticalalignment='center',
        #         fontsize=FONT_SECTION[1], color='gray', transform=ax.transAxes)

        # Categories moved under the graph, horizontal, and smaller
        # loc='upper center' and bbox_to_anchor=(0.5, -0.05) to position it slightly below the chart area (relative to axes)
        # ncol=len(labels) for horizontal arrangement
        # fontsize reduced for smaller text
        ax.legend(wedges, labels, title="Categories", loc='upper center', bbox_to_anchor=(0.5, 0.05),
                  fancybox=True, shadow=True, ncol=len(labels), frameon=True,
                  fontsize=7, title_fontsize=9)

    plt.tight_layout(pad=0.5)  # Increased pad to give space for the legend at the bottom

    if canvas_chart_widget_ref:
        canvas_chart_widget_ref.destroy()

    canvas_chart_agg = FigureCanvasTkAgg(fig, master=pie_chart_section_canvas)
    canvas_chart_widget = canvas_chart_agg.get_tk_widget()
    canvas_chart_widget.config(bg=pie_chart_section_canvas['bg'])  # Ensured widget background matches parent canvas

    # Place chart widget in the middle of the defined chart_display_height area
    chart_widget_center_y = chart_top_y + chart_display_height / 2
    pie_chart_section_canvas.create_window(current_width / 2, chart_widget_center_y, window=canvas_chart_widget,
                                           anchor="center")
    canvas_chart_widget_ref = canvas_chart_widget

    # Update total savings label to show actual total savings
    total_savings_amount_lbl_widget_ref.config(
        text=f"Total Savings: ₱{total_savings_for_month:,.2f}",  # Display actual total
        justify=tk.CENTER
    )
    # Reposition and raise total expenses label using its canvas ID
    pie_chart_section_canvas.delete("total_savings_label")  # Remove old one if exists before recreating
    pie_chart_section_canvas.create_window(current_width / 2, current_height - 30,  # Position near the bottom center
        window=total_savings_amount_lbl_widget_ref, anchor="s", tags="total_savings_label"
    )
    pie_chart_section_canvas.tag_raise("total_savings_label")  # Ensure it's on top

    # --- Hover Logic for Pie Chart ---
    # Attach annotation object to the axis for persistence
    if not hasattr(ax, '_hover_annotation'):
        ax._hover_annotation = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                           bbox=dict(boxstyle="round,pad=0.5", fc="lightyellow", ec="k", lw=1),
                                           arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3"),
                                           visible=False)
    annot = ax._hover_annotation

    # Store data for hover (these are the current state of pie elements)
    pie_elements_data = {
        'wedges': wedges,
        'labels': labels,
        'sizes': sizes,
        'autotexts': autotexts
    }

    def update_annot(idx):
        if pie_elements_data['wedges'] and idx < len(pie_elements_data['wedges']):
            wedge = pie_elements_data['wedges'][idx]
            label = pie_elements_data['labels'][idx]
            size = pie_elements_data['sizes'][idx]
            total = sum(pie_elements_data['sizes']) if sum(pie_elements_data['sizes']) > 0 else 1
            percentage = (size / total) * 100

            annot.xy = wedge.center  # Position the annotation at the wedge center
            text = f"{label}\n₱{size:,.2f} ({percentage:.1f}%)"
            annot.set_text(text)
            annot.set_visible(True)
        else:
            annot.set_visible(False)

    def hover_pie(event):
        if event.inaxes == ax:  # Check if mouse is within the axes
            contained = False
            for i, wedge in enumerate(pie_elements_data['wedges']):
                if wedge.contains(event)[0]:  # contains returns (bool, dict)
                    update_annot(i)
                    contained = True
                    break
            if not contained:
                annot.set_visible(False)
            fig.canvas.draw_idle()  # Redraw the figure only when necessary
        else:
            if annot:  # Check if annot exists before trying to hide
                annot.set_visible(False)
            fig.canvas.draw_idle()  # Redraw to hide annotation

    # Connect the hover event to the figure's canvas
    fig.canvas.mpl_connect("motion_notify_event", hover_pie)

    plt.close(fig)  # Close the figure to free up memory once embedded


def update_recent_transaction_box(event=None):  # Make event optional
    """
    Updates the content of the right-side recent transactions box on resize.
    Now ensures the combobox and add button persist by not deleting them.
    """
    global recent_transaction_canvas  # Ensure this is accessible
    global recent_transaction_category_combobox, recent_transaction_category_combobox_window_id, add_button_ref, add_button_window_id, recent_transaction_category_combobox_var
    global logged_in_user_id  # Ensure user_id is accessible

    if not recent_transaction_canvas:
        return

    # !!! CRITICAL CHANGE: Only delete specific items, not "all" !!!
    # Delete previous transaction list items, watermark, and static text if they are being redrawn.
    recent_transaction_canvas.delete("transaction_item")
    recent_transaction_canvas.delete("watermark")
    recent_transaction_canvas.delete("static_text")  # Tag for titles and headers

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
                                          font=("Arial", int(current_height * 0.7 * 0.5), "bold"),  # Adjusted font size
                                          fill="#f0f0f0", anchor="center", tags="watermark")
    recent_transaction_canvas.tag_lower("watermark")

    # 3. Draw other static foreground content (titles/headers) using tags for selective deletion
    recent_transaction_canvas.create_text(20, 20, anchor="nw", text="Recent Savings", font=FONT_SECTION,
                                          fill="black", tags="static_text")  # Tagged
    recent_transaction_canvas.create_text(current_width - 30, 60, anchor="ne", text="Amount", font=FONT_SUBTEXT,
                                          fill="black", tags="static_text")  # Tagged

    # Add Button (text-based) - ENSURE POSITION IS UPDATED
    # The button is created once in create_total_savings_app, so just update its position
    recent_transaction_canvas.coords(add_button_window_id, current_width - 30, 20)
    recent_transaction_canvas.tag_raise(add_button_window_id)

    # --- Category Dropdown --- ENSURE POSITION AND VALUES ARE UPDATED
    # The combobox is created once in create_total_savings_app.
    # Update values in combobox in case new categories were added
    # MODIFIED: If get_all_savings needs user_id, pass it here:
    # categories_from_db = sorted(list(set(item[1] for item in database_manager.get_all_savings(logged_in_user_id))))
    categories_from_db = sorted(
        list(set(item[1] for item in database_manager.get_all_savings())))
    categories_for_filter = ["All Categories"] + categories_from_db

    recent_transaction_category_combobox['values'] = categories_for_filter
    # Ensure the current selection is still valid after updating values
    if recent_transaction_category_combobox_var.get() not in categories_for_filter:
        recent_transaction_category_combobox_var.set("All Categories")

    # Update combobox position
    recent_transaction_canvas.coords(recent_transaction_category_combobox_window_id, 30,
                                     60)  # Corrected coords for combobox
    recent_transaction_canvas.tag_raise(recent_transaction_category_combobox_window_id)

    # --- Fetch recent savings from database and apply filter ---
    selected_filter_category = recent_transaction_category_combobox_var.get()
    # MODIFIED: If get_all_savings needs user_id, pass it here:
    # all_savings = database_manager.get_all_savings(logged_in_user_id)
    all_savings = database_manager.get_all_savings()

    if selected_filter_category != "All Categories":
        filtered_savings = [s for s in all_savings if s[1] == selected_filter_category]
    else:
        filtered_savings = all_savings

    # --- Draw column headers ONCE, before the loop ---
    col2_x = int(current_width * 0.55)
    col3_x = current_width - 30

    recent_transaction_canvas.create_text(col2_x, 75, anchor="center", text="Date", font=FONT_SUBTEXT,
                                          fill="black", tags="static_text")
    recent_transaction_canvas.create_text(col3_x, 75, anchor="e", text="Amount", font=FONT_SUBTEXT,
                                          fill="black", tags="static_text")

    # --- Now draw the data rows ---
    y_offset = 110
    line_height = 30
    display_limit = int((current_height - y_offset - 30) / line_height)

    if not filtered_savings:
        recent_transaction_canvas.create_text(
            current_width / 2, y_offset + line_height,
            anchor="center",
            text="No Recent Savings",
            font=FONT_SUBTEXT,
            fill="gray",
            tags="transaction_item"
        )
    else:
        for idx, (id, category, amount, transaction_date_str) in enumerate(filtered_savings):
            if idx >= display_limit:
                break

            display_amount = f"₱{amount:,.2f}"
            try:
                dt_obj = datetime.strptime(transaction_date_str, "%Y-%m-%d %H:%M:%S")
                display_date = dt_obj.strftime("%b %d, %Y")
            except ValueError:
                display_date = "Invalid Date"

            # Added "category_link" tag for clickability
            recent_transaction_canvas.create_text(60, y_offset, anchor="w", text=category,
                                                  font=FONT_TRANSACTION, fill="black",
                                                  tags=("transaction_item", "category_link"))
            recent_transaction_canvas.create_text(col2_x, y_offset, anchor="center", text=display_date,
                                                  font=FONT_TRANSACTION, fill="black", tags="transaction_item")
            recent_transaction_canvas.create_text(col3_x, y_offset, anchor="e", text=display_amount,
                                                  font=FONT_TRANSACTION, fill="black", tags="transaction_item")
            y_offset += line_height


# Helper functions for hover effects (moved outside lambda)
def _on_enter_menu_item(event, canvas_widget, item_text, current_page_name):
    # Change background of the canvas only if not the current page
    if item_text != current_page_name:
        canvas_widget.config(bg="#e0e0e0")


def _on_leave_menu_item(event, canvas_widget, item_text, current_page_name):
    # Revert background of the canvas
    if item_text != current_page_name:
        canvas_widget.config(bg=COLOR_SIDEBAR)


# Helper function to create menu items with icons
def create_icon_menu(parent, text, command):
    global sidebar_icons  # Access the global icon dictionary
    # Adjusted width and height for larger boxes
    canvas = tk.Canvas(parent, width=SIDEBAR_WIDTH - 60, height=140, bg=COLOR_SIDEBAR, highlightthickness=0)
    r = 35  # Increased radius for more rounded corners on larger box
    icon_x_offset = 25  # Adjusted x-offset
    icon_y_offset = 25  # Adjusted y-offset
    icon_box_width = 140  # Increased icon box width
    icon_box_height = 110  # Increased icon box height

    # Draw rounded box for the icon
    canvas.create_arc(icon_x_offset, icon_y_offset, icon_x_offset + 2 * r, icon_y_offset + 2 * r,
                      start=90, extent=90, fill=COLOR_NAVBAR, outline=COLOR_NAVBAR)
    canvas.create_arc(icon_x_offset + icon_box_width - 2 * r, icon_y_offset, icon_x_offset + icon_box_width,
                      icon_y_offset + 2 * r,
                      start=0, extent=90, fill=COLOR_NAVBAR, outline=COLOR_NAVBAR)
    canvas.create_arc(icon_x_offset, icon_y_offset + icon_box_height - 2 * r, icon_x_offset + 2 * r,
                      icon_y_offset + icon_box_height,
                      start=180, extent=90, fill=COLOR_NAVBAR, outline=COLOR_NAVBAR)
    canvas.create_arc(icon_x_offset + icon_box_width - 2 * r, icon_y_offset + icon_box_height - 2 * r,
                      icon_x_offset + icon_box_width, icon_y_offset + icon_box_height,
                      start=270, extent=90, fill=COLOR_NAVBAR, outline=COLOR_NAVBAR)
    canvas.create_rectangle(icon_x_offset + r, icon_y_offset, icon_x_offset + icon_box_width - r,
                            icon_y_offset + icon_box_height,
                            fill=COLOR_NAVBAR, outline=COLOR_NAVBAR)
    canvas.create_rectangle(icon_x_offset, icon_y_offset + r, icon_x_offset + icon_box_width,
                            icon_y_offset + icon_box_height - r,
                            fill=COLOR_NAVBAR, outline=COLOR_NAVBAR)

    # Place the image in the center of the rounded box
    if sidebar_icons.get(text):
        canvas.create_image(icon_x_offset + icon_box_width // 2, icon_y_offset + icon_box_height // 2,
                            image=sidebar_icons[text], anchor="center")
    else:
        # Placeholder text if image fails to load
        canvas.create_text(icon_x_offset + icon_box_width // 2, icon_y_offset + icon_box_height // 2,
                           text="?", font=("Arial", 24), fill="gray", anchor="center")  # Larger placeholder font

    # Place the label to the right of the icon box
    label_x = icon_x_offset + icon_box_width + 20
    # Corrected label_y for vertical centering
    label_y = canvas.winfo_height() * 80  # Corrected this line for proper vertical centering
    label_width = SIDEBAR_WIDTH - label_x - 30  # Adjusted for padding

    canvas.create_text(
        label_x, label_y,
        text=text,
        font=FONT_MENU,
        fill="black",
        anchor="w",
        width=label_width  # Enables text wrapping
    )

    # Bind click event to the canvas
    canvas.bind("<Button-1>", lambda e: command())
    # Bind hover events to call the helper functions
    canvas.bind("<Enter>", lambda e, c=canvas, t=text, cp="Total Savings": _on_enter_menu_item(e, c, t, cp))
    canvas.bind("<Leave>", lambda e, c=canvas, t=text, cp="Total Savings": _on_leave_menu_item(e, c, t, cp))

    return canvas


def create_total_savings_app():
    global root_window, month_var, recent_transaction_category_combobox_var
    global pie_chart_section_canvas, recent_transaction_canvas, top_right_header_canvas
    global month_combo_widget_ref, total_savings_amount_lbl_widget_ref
    global recent_transaction_category_combobox, recent_transaction_category_combobox_window_id, add_button_ref, add_button_window_id
    global logged_in_user_id, logged_in_username
    global tracku_label_tk, total_savings_header_label_tk  # Ensure these are global for initial creation
    global welcome_label_ref  # Global reference for welcome label
    global sidebar_icons  # Make sidebar_icons global

    root_window = tk.Tk()
    root_window.title("TrackU - Total Savings")
    root_window.state("zoomed")
    root_window.configure(bg=COLOR_BG)

    # Initialize the database (IMPORTANT: This ensures the DB exists and tables are created)
    database_manager.initialize_db()

    # --- Retrieve User ID from command line arguments ---
    if len(sys.argv) > 1:
        try:
            logged_in_user_id = int(sys.argv[1])
            fetched_username = database_manager.get_username_by_id(logged_in_user_id)
            if fetched_username:
                logged_in_username = fetched_username
            else:
                print(f"Warning: User with ID {logged_in_user_id} not found in database. Running as 'Guest'.")
                logged_in_user_id = None
        except ValueError:
            print("Error: Invalid user ID provided as command-line argument. Running as 'Guest'.")
            logged_in_user_id = None
    else:
        print("No user ID provided as command-line argument for Savings. Running as guest or default user.")

    root_window.grid_columnconfigure(0, weight=0, minsize=250)
    root_window.grid_columnconfigure(1, weight=1)
    root_window.grid_rowconfigure(0, weight=0, minsize=85)
    root_window.grid_rowconfigure(1, weight=1)

    # --- Initialize global StringVars BEFORE widgets are created ---
    month_var = tk.StringVar(value=calendar.month_name[datetime.now().month])
    recent_transaction_category_combobox_var = tk.StringVar(value="All Categories")
    # ---------------------------------------------------------------

    # --- LEFT SIDEBAR FRAME ---
    sidebar_frame = tk.Frame(root_window, bg=COLOR_SIDEBAR, width=SIDEBAR_WIDTH, highlightthickness=0)
    sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
    sidebar_frame.grid_propagate(False)
    sidebar_frame.grid_columnconfigure(0, weight=1)

    # Define icon paths relative to the script's directory (TOTAL SAVINGS)
    # Corrected icon paths to include 'icons' subdirectory for better organization
    icon_paths = {
        "Dashboard": os.path.join(current_script_dir, "..", "DASHBOARD","dashboard.png"),
        "Total Savings": os.path.join(current_script_dir,"piggy-bank.png"),  # Icon specific to current app
        "Total Expenses": os.path.join(current_script_dir, "..", "TOTAL EXPENSES", "spending.png"),
        "Profile": os.path.join(current_script_dir, "user.png")
    }

    # Load sidebar icons once during app creation
    for key, path in icon_paths.items():
        try:
            if os.path.exists(path):
                img = Image.open(path).resize(ICON_SIZE, Image.LANCZOS)
                sidebar_icons[key] = ImageTk.PhotoImage(img)
            else:
                sidebar_icons[key] = None
                print(f"Warning: Icon '{path}' not found.")
        except Exception as e:
            sidebar_icons[key] = None
            print(f"Error loading icon '{path}': {e}")

    # Placing the main TrackU logo at the top of the sidebar
    global sidebar_logo_img_main  # New global reference for the main logo
    sidebar_logo_img_main = None
    try:
        logo_path_attempt = os.path.join(current_script_dir, "testlogo.png")
        if not os.path.exists(logo_path_attempt):
            # Also check in a common 'icons' subdirectory
            logo_path_attempt = os.path.join(current_script_dir, "icons", "testlogo.png")

        if os.path.exists(logo_path_attempt):
            img = Image.open(logo_path_attempt).resize(LOGO_SIZE_SIDEBAR, Image.LANCZOS)
            sidebar_logo_img_main = ImageTk.PhotoImage(img)  # Store in new global ref
            logo_label = tk.Label(sidebar_frame, image=sidebar_logo_img_main, bg=COLOR_SIDEBAR, borderwidth=0)
            logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
        else:
            logo_label = tk.Label(sidebar_frame, text="TrackU Logo", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR,
                                  fg="darkgray")
            logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
            print("Warning: testlogo.png not found for main sidebar logo. Using placeholder text.")
    except Exception as e:
        print(f"Error loading main sidebar logo: {e}. Using placeholder text.")
        logo_label = tk.Label(sidebar_frame, text="TrackU Logo", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR,
                              fg="darkgray")
        logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")

    menu_items = [
        ("Dashboard"),
        ("Total Savings"),
        ("Total Expenses"),
        ("Profile"),
    ]

    # Dynamically calculate rows for proper spacing
    total_menu_items = len(menu_items)
    sidebar_frame.grid_rowconfigure(0, weight=0)  # For the TrackU logo
    for i in range(1, total_menu_items + 1):
        sidebar_frame.grid_rowconfigure(i, weight=0)  # For each menu item
    sidebar_frame.grid_rowconfigure(total_menu_items + 1, weight=1)  # To push last item down if needed

    for idx, label_text in enumerate(menu_items):
        menu_canvas = create_icon_menu(sidebar_frame, label_text,
                                       lambda item=label_text: on_menu_item_click(item, root_window))
        # Highlight current page button
        if label_text == "Total Savings":
            menu_canvas.config(bg=COLOR_NAVBAR)  # Highlight the current page
        menu_canvas.grid(row=idx + 1, column=0, pady=8, padx=8, sticky="ew")

    # Add a spacer to push content to the top
    tk.Label(sidebar_frame, text="", bg=COLOR_SIDEBAR).grid(row=len(menu_items) + 1, column=0, sticky="nsew")
    sidebar_frame.grid_rowconfigure(len(menu_items) + 1, weight=1)

    # --- TOP RIGHT HEADER / NAVBAR ---
    top_right_header_canvas = tk.Canvas(root_window, bg=COLOR_BG, height=110, highlightthickness=0)
    top_right_header_canvas.grid(row=0, column=1, sticky="nsew")

    # Create initial header labels here
    tracku_label_tk = tk.Label(top_right_header_canvas, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
    total_savings_header_label_tk = tk.Label(top_right_header_canvas, text="Total Savings", font=("Georgia", 16),
                                             bg=COLOR_NAVBAR, fg="#222")
    top_right_header_canvas.bind("<Configure>", draw_top_right_header_content)

    # --- MAIN CONTENT FRAME ---
    main_content_area = tk.Frame(root_window, bg=COLOR_BG)
    main_content_area.grid(row=1, column=1, sticky="nsew", padx=30, pady=20)
    main_content_area.grid_columnconfigure(0, weight=1, minsize=300)
    main_content_area.grid_columnconfigure(1, weight=1)
    main_content_area.grid_rowconfigure(0, weight=0)  # Welcome label row
    main_content_area.grid_rowconfigure(1, weight=1)  # Charts/Transactions row

    # Welcome Label (similar to dashboard, placed at the top of the main content area)
    # welcome_label_ref = tk.Label(main_content_area, text=f"Welcome, {logged_in_username}", font=FONT_WELCOME,
    #                              bg=COLOR_BG)
    # welcome_label_ref.grid(row=0, column=0, columnspan=2, sticky="w", padx=(0, 0), pady=(0, 10))

    # --- Container for Pie Chart and Recent Transactions ---
    charts_transactions_container = tk.Frame(main_content_area, bg=COLOR_BG)
    charts_transactions_container.grid(row=1, column=0, columnspan=2, sticky="nsew")
    charts_transactions_container.grid_columnconfigure(0, weight=1)
    charts_transactions_container.grid_columnconfigure(1, weight=1)
    charts_transactions_container.grid_rowconfigure(0, weight=1)

    # --- LEFT SECTION: Pie Chart and Savings Details ---
    pie_chart_section_canvas = tk.Canvas(charts_transactions_container, bg=COLOR_BG, highlightthickness=0)
    pie_chart_section_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=10)

    # Month combobox for pie chart - CREATED ONCE HERE
    months = [calendar.month_name[i] for i in range(1, 13)]
    month_combo_widget_ref = ttk.Combobox(pie_chart_section_canvas, textvariable=month_var, values=months,
                                          state="readonly", font=FONT_SUBTEXT, justify="center", width=15)
    month_combo_widget_ref.current(datetime.now().month - 1)
    month_combo_widget_ref.bind("<<ComboboxSelected>>", lambda e: refresh_data_and_ui())

    # Total savings amount label - CREATED ONCE HERE
    total_savings_amount_lbl_widget_ref = tk.Label(pie_chart_section_canvas, text="Total Savings: Total.",
                                                   font=("Georgia", 13), bg=COLOR_BG, fg="black",
                                                   justify=tk.CENTER)  # Changed text and justify

    pie_chart_section_canvas.bind("<Configure>", update_pie_chart_section)  # Bind to general update

    # --- RIGHT SECTION: Recent Savings ---
    recent_transaction_canvas = tk.Canvas(charts_transactions_container, bg=COLOR_BG, highlightthickness=0)
    recent_transaction_canvas.grid(row=0, column=1, sticky="nsew", pady=10)

    # ADDED: Bind the click handler to the recent_transaction_canvas
    recent_transaction_canvas.bind("<Button-1>", on_recent_transaction_canvas_click)

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
    root_window.update_idletasks()  # Ensure sizes are calculated before initial placement
    initial_canvas_width = recent_transaction_canvas.winfo_width()
    add_button_window_id = recent_transaction_canvas.create_window(
        initial_canvas_width - 30, 20, window=add_button_ref, anchor="ne"
    )

    # Category Combobox for Recent Transactions - CREATED ONCE HERE
    categories_from_db = sorted(list(set(item[1] for item in database_manager.get_all_savings())))
    categories_for_filter = ["All Categories"] + categories_from_db
    recent_transaction_category_combobox = ttk.Combobox(
        recent_transaction_canvas,
        textvariable=recent_transaction_category_combobox_var,  # Use global StringVar
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
        30, 60, window=recent_transaction_category_combobox, anchor="nw"
    )

    recent_transaction_canvas.bind("<Configure>", update_recent_transaction_box)

    # Initial call to populate data after all widgets are set up
    root_window.update_idletasks()  # Ensure sizes are calculated before initial draw
    refresh_data_and_ui()

    root_window.mainloop()


if __name__ == "__main__":
    create_total_savings_app()
