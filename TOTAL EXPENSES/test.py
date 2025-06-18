import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import os

# --- Colors ---
COLOR_BG = "#fdfdf5"
COLOR_NAVBAR = "#ffe0b2"  # Top right header color
COLOR_SIDEBAR = "#d6e9d5"  # Sidebar color
COLOR_CANVAS_BAR = "#fdf6e3"  # Background for the recent transactions box (still used for fill)
# COLOR_BOX_BORDER = "black" # Removed as borders are being removed
COLOR_PIE_SLICE_1 = "#4dd0e1"  # Teal
COLOR_PIE_SLICE_2 = "#ff8a65"  # Orange
COLOR_PIE_SLICE_3 = "#ffd54f"  # Red/Yellow

# --- Fonts ---
FONT_BRAND = ("Playfair Display", 20, "bold")
FONT_MENU = ("Playfair Display", 13)
FONT_SECTION = ("Georgia", 16, "bold")
FONT_SUBTEXT = ("Playfair Display", 12)
FONT_TRANSACTION = ("Playfair Display", 11)

# Dummy data for transactions
transactions = [
    ("Food", "-100"),
    ("School Supplies", "-100"),
    ("Emergency Funds", "-100"),
    ("School Fees", "-100"),
    ("Food", "-100"),
    ("General Savings", "-100"),
    ("Personal Goal", "-100"),
    ("Future Purchases", "-100"),
]

# Global image references to prevent garbage collection (for sidebar icons)
sidebar_icon_refs = {}


# --- Helper Function for Sidebar Items ---
def create_sidebar_item(parent_frame, text, icon_name, row_index, command=None):
    item_frame = tk.Frame(parent_frame, bg=COLOR_SIDEBAR)
    item_frame.grid(row=row_index, column=0, sticky="ew", padx=10, pady=5)
    item_frame.grid_columnconfigure(1, weight=1)

    icon_path = os.path.join("icons", f"{icon_name}.png")

    icon_label = None
    try:
        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize((30, 30), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            sidebar_icon_refs[text] = photo
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
    # If outline_width is 0, don't draw an outline
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
total_expenses_label_tk = None


def draw_top_right_header_content(event):
    """Draws the custom rounded rectangle and places content on the top right header canvas."""
    global tracku_label_tk, total_expenses_label_tk
    top_right_header_canvas.delete("all")
    draw_bottom_rounded_rect(top_right_header_canvas, 0, 0, event.width, event.height, 20, COLOR_NAVBAR)

    if tracku_label_tk is None:
        tracku_label_tk = tk.Label(top_right_header_canvas, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
        total_expenses_label_tk = tk.Label(top_right_header_canvas, text="Total Expenses", font=("Georgia", 16),
                                           bg=COLOR_NAVBAR, fg="#222")

    top_right_header_canvas.create_window(30, event.height / 2, window=tracku_label_tk, anchor="w")
    top_right_header_canvas.create_window(event.width - 30, event.height / 2, window=total_expenses_label_tk,
                                          anchor="e")


# Global reference for the matplotlib canvas widget
canvas_chart_widget_ref = None


def update_pie_chart_section(event, canvas, month_combobox, total_expenses_lbl):
    """Updates the content of the left-side section (month, pie chart, expenses)."""
    global canvas_chart_widget_ref
    canvas.delete("all")  # Clear the canvas

    current_width = event.width
    current_height = event.height

    # Position month combobox (top-left)
    canvas.create_window(current_width * 0.15, 40, window=month_combobox, anchor="w")

    # --- Matplotlib Pie Chart ---
    chart_height_ratio = 0.6
    fig, ax = plt.subplots(figsize=(current_width / 80, (current_height * chart_height_ratio) / 80), dpi=80,
                           facecolor=COLOR_BG)
    sizes = [50, 30, 20]
    colors = [COLOR_PIE_SLICE_1, COLOR_PIE_SLICE_2, COLOR_PIE_SLICE_3]
    explode = (0.02, 0.02, 0.02)

    ax.pie(sizes, colors=colors, explode=explode, startangle=140, wedgeprops=dict(width=0.8, edgecolor=COLOR_BG))
    ax.axis('equal')
    ax.set_facecolor(COLOR_BG)
    plt.tight_layout(pad=0)

    ax.text(0, 0, 'Category', horizontalalignment='center', verticalalignment='center',
            fontsize=FONT_SECTION[1], color='gray', transform=ax.transAxes)

    if canvas_chart_widget_ref:
        canvas_chart_widget_ref.destroy()

    canvas_chart_agg = FigureCanvasTkAgg(fig, master=canvas)
    canvas_chart_widget = canvas_chart_agg.get_tk_widget()
    canvas_chart_widget.config(bg=COLOR_BG)

    chart_center_y = current_height * (0.15 + chart_height_ratio / 2)
    canvas.create_window(current_width / 2, chart_center_y, window=canvas_chart_widget, anchor="center")
    canvas_chart_widget_ref = canvas_chart_widget

    total_expenses_y = current_height * (0.15 + chart_height_ratio) + 30
    canvas.create_window(current_width / 2, total_expenses_y, window=total_expenses_lbl, anchor="n")

    plt.close(fig)


# Global variable for the category combobox in recent transactions
recent_transaction_category_combobox = None


def update_recent_transaction_box(event):
    """Updates the content of the right-side recent transactions box on resize."""
    global recent_transaction_category_combobox
    recent_transaction_canvas.delete("all")
    current_width = event.width
    current_height = event.height

    # 1. Draw the main rounded rectangle background WITHOUT outline
    draw_rounded_rect(recent_transaction_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR,
                      outline_width=0)

    # 2. Peso sign watermark (faded in background) - DRAW THIS NOW
    # It will be behind subsequent text but in front of the box drawn above.
    recent_transaction_canvas.create_text(current_width / 2, current_height / 2, text="₱",
                                          font=("Arial", int(current_height * 0.7), "bold"),
                                          fill="#f0f0e0", anchor="center", tags="watermark")

    # 3. Header: "Recent Transaction" and "+" icon
    recent_transaction_canvas.create_text(20, 20, anchor="nw", text="Recent Transaction", font=FONT_SECTION,
                                          fill="black")
    recent_transaction_canvas.create_text(current_width - 30, 20, anchor="ne", text="+", font=("Arial", 28, "bold"),
                                          fill="black")

    # Column Headers: "Amount" (Category is handled by the dropdown)
    recent_transaction_canvas.create_text(current_width - 30, 60, anchor="ne", text="Amount", font=FONT_SUBTEXT,
                                          fill="black")

    # Category Dropdown
    if recent_transaction_category_combobox is None or not recent_transaction_category_combobox.winfo_exists():
        recent_transaction_category_combobox_var = tk.StringVar(value="Category")
        recent_transaction_category_combobox = ttk.Combobox(
            recent_transaction_canvas,
            textvariable=recent_transaction_category_combobox_var,
            values=["Category", "Food", "School Supplies", "Emergency Funds", "School Fees", "General Savings",
                    "Personal Goal", "Future Purchases"],
            state="readonly",
            width=10,
            font=FONT_SUBTEXT,
            justify="center"
        )
    recent_transaction_canvas.create_window(70, 60, window=recent_transaction_category_combobox, anchor="w")

    # Transaction list
    y_offset = 90
    line_height = 28
    for idx, (category, amount) in enumerate(transactions):
        if y_offset + line_height > current_height - 30:
            break
        recent_transaction_canvas.create_text(30, y_offset, anchor="w", text=f"• {category}", font=FONT_TRANSACTION,
                                              fill="black")
        recent_transaction_canvas.create_text(current_width - 30, y_offset, anchor="e", text=f"{amount}",
                                              font=FONT_TRANSACTION, fill="black")
        y_offset += line_height


# --- Main App Window ---
root = tk.Tk()
root.title("TrackU")
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

sidebar_items_data = [
    ("Dashboard", "dashboard"),
    ("Total Savings", "savings"),
    ("Total Expenses", "expenses"),
    ("Profile", "profile")
]

row_idx = 0
for text, icon_name in sidebar_items_data:
    create_sidebar_item(sidebar_frame, text, icon_name, row_idx)
    row_idx += 1

sidebar_frame.grid_rowconfigure(row_idx, weight=1)

# --- TOP RIGHT HEADER / NAVBAR (Canvas for drawing rounded bottom corners) ---
top_right_header_canvas = tk.Canvas(root, bg=COLOR_BG, height=70, highlightthickness=0)
top_right_header_canvas.grid(row=0, column=1, sticky="nsew")
top_right_header_canvas.bind("<Configure>", draw_top_right_header_content)

# --- MAIN CONTENT FRAME (Placed in row 1, column 1, below the top right header) ---
main_content_area = tk.Frame(root, bg=COLOR_BG)
main_content_area.grid(row=1, column=1, sticky="nsew", padx=30, pady=20)
main_content_area.grid_columnconfigure(0, weight=1, minsize=300)
main_content_area.grid_columnconfigure(1, weight=1)
main_content_area.grid_rowconfigure(0, weight=1)

# --- LEFT SECTION: Pie Chart and Expense Details ---
pie_chart_section_canvas = tk.Canvas(main_content_area, bg=COLOR_BG, highlightthickness=0)
pie_chart_section_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=10)

# --- MODIFIED CODE FOR MONTHS DROPDOWN ---
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

month_var = tk.StringVar(value="January") # Set initial value to January
month_combo = ttk.Combobox(pie_chart_section_canvas, textvariable=month_var, values=months,
                           state="readonly", font=FONT_SUBTEXT, justify="center", width=10) # Adjust width if needed

# Set default selection
month_combo.current(0)
# --- END MODIFIED CODE ---


total_expenses_amount_lbl = tk.Label(pie_chart_section_canvas, text="Total Expenses:\n₱ 100,000.00",
                                     font=("Georgia", 13), bg=COLOR_BG, fg="black", justify=tk.LEFT)

pie_chart_section_canvas.bind("<Configure>",
                              lambda event: update_pie_chart_section(event, pie_chart_section_canvas, month_combo,
                                                                     total_expenses_amount_lbl))

# --- RIGHT SECTION: Recent Transactions ---
recent_transaction_canvas = tk.Canvas(main_content_area, bg=COLOR_BG, highlightthickness=0)
recent_transaction_canvas.grid(row=0, column=1, sticky="nsew", pady=10)

recent_transaction_category_combobox_var = tk.StringVar(value="Category")
recent_transaction_category_combobox = ttk.Combobox(
    recent_transaction_canvas,
    textvariable=recent_transaction_category_combobox_var,
    values=["Category", "Food", "School Supplies", "Emergency Funds", "School Fees", "General Savings", "Personal Goal",
            "Future Purchases"],
    state="readonly",
    width=10,
    font=FONT_SUBTEXT,
    justify="center"
)

recent_transaction_canvas.bind("<Configure>", update_recent_transaction_box)

root.mainloop()