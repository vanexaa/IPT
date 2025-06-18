import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import pyglet
import os
import subprocess
import sys

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
COLOR_BOX_BORDER = "black"

# --- Fonts ---
FONT_BRAND = ("Playfair Display", 20, "bold")
FONT_MENU = ("Playfair Display", 13)
FONT_SECTION = ("Georgia", 16, "bold")
FONT_SUBTEXT = ("Playfair Display", 12)
FONT_TRANSACTION = ("Playfair Display", 11)

LOGO_SIZE_SIDEBAR = (150, 100)

transactions = [
    ("Groceries", "-1500"),
    ("Utilities", "-300"),
    ("Rent", "-5000"),
    ("Transportation", "-250"),
    ("Dining Out", "-400"),
    ("Entertainment", "-180"),
    ("Miscellaneous", "-120"),
]

sidebar_icon_refs = {}

def on_menu_item_click(item_name, current_root):
    script_dir = os.path.dirname(__file__)
    script_to_launch = None
    if item_name == "Dashboard":
        script_to_launch = os.path.join(script_dir, "..", "DASHBOARD", "dashboard.py")
    elif item_name == "Total Expenses":
        script_to_launch = os.path.join(script_dir, "expenses.py")
    elif item_name == "Total Savings":
        script_to_launch = os.path.join(script_dir, "..", "TOTAL SAVINGS", "savings.py")
    elif item_name == "Profile":
        return
    if script_to_launch:
        try:
            subprocess.Popen(
                [sys.executable, script_to_launch],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        except Exception as e:
            print(f"Failed to launch: {e}")
    current_root.destroy()

def create_sidebar_item(parent_frame, text, icon_name, row_index, command=None):
    item_frame = tk.Frame(parent_frame, bg=COLOR_SIDEBAR)
    item_frame.grid(row=row_index, column=0, sticky="ew", padx=10, pady=5)
    item_frame.grid_columnconfigure(1, weight=1)
    script_dir = os.path.dirname(__file__)
    icon_path = os.path.join(script_dir, "icons", f"{icon_name}.png")
    icon_label = None
    try:
        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize((30, 30), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            sidebar_icon_refs[text] = photo
            icon_label = tk.Label(item_frame, image=photo, bg=COLOR_SIDEBAR)
        else:
            icon_label = tk.Label(item_frame, text="[I]", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR, fg="black")
    except Exception as e:
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

def draw_bottom_rounded_rect(canvas, x, y, w, h, r, color):
    canvas.create_rectangle(x, y, x + w, y + r, fill=color, outline=color)
    canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)
    canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x + r, y + h - r, x + w - r, y + h, fill=color, outline=color)

def draw_rounded_rect(canvas, x, y, w, h, r, color, outline_color="", outline_width=0):
    if outline_width > 0 and outline_color:
        canvas.create_arc(x, y, x + 2 * r, y + 2 * r, start=90, extent=90, fill=color, outline=outline_color, width=outline_width)
        canvas.create_arc(x + w - 2 * r, y, x + w, y + 2 * r, start=0, extent=90, fill=color, outline=outline_color, width=outline_width)
        canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=outline_color, width=outline_width)
        canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=outline_color, width=outline_width)
        canvas.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=outline_color, width=outline_width)
        canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=outline_color, width=outline_width)
    else:
        canvas.create_arc(x, y, x + 2 * r, y + 2 * r, start=90, extent=90, fill=color, outline=color)
        canvas.create_arc(x + w - 2 * r, y, x + w, y + 2 * r, start=0, extent=90, fill=color, outline=color)
        canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color)
        canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
        canvas.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color)
        canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)

tracku_label_tk = None
total_expenses_header_label_tk = None

def draw_top_right_header_content(event):
    global tracku_label_tk, total_expenses_header_label_tk
    top_right_header_canvas.delete("all")
    draw_bottom_rounded_rect(top_right_header_canvas, 0, 0, event.width, event.height, 20, COLOR_NAVBAR)
    if tracku_label_tk is None:
        tracku_label_tk = tk.Label(top_right_header_canvas, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
        total_expenses_header_label_tk = tk.Label(top_right_header_canvas, text="Total Expenses", font=("Georgia", 16), bg=COLOR_NAVBAR, fg="#222")
    top_right_header_canvas.create_window(30, event.height / 2, window=tracku_label_tk, anchor="w")
    top_right_header_canvas.create_window(event.width - 30, event.height / 2, window=total_expenses_header_label_tk, anchor="e")

canvas_chart_widget_ref = None

def update_pie_chart_section(event, canvas, month_combobox, total_expenses_lbl):
    global canvas_chart_widget_ref
    canvas.delete("all")
    current_width = event.width
    current_height = event.height
    canvas.create_text(current_width / 2, current_height / 2, text="₱", font=("Arial", int(current_height * 0.7), "bold"), fill="#f0f0e0", anchor="center", tags="pie_watermark")
    canvas.tag_lower("pie_watermark")
    canvas.create_window(current_width / 2, 40, window=month_combobox, anchor="n")
    chart_height_ratio = 0.6
    fig, ax = plt.subplots(figsize=(current_width / 100, (current_height * chart_height_ratio) / 100), dpi=100, facecolor=COLOR_BG)
    sizes = [40, 30, 20, 10]
    colors = [COLOR_PIE_SLICE_1, COLOR_PIE_SLICE_2, COLOR_PIE_SLICE_3, "#90a4ae"]
    explode = (0.02, 0.02, 0.02, 0.02)
    ax.pie(sizes, colors=colors, explode=explode, startangle=140, wedgeprops=dict(width=0.8, edgecolor=COLOR_BG))
    ax.axis('equal')
    ax.set_facecolor(COLOR_BG)
    plt.tight_layout(pad=0)
    ax.text(0, 0, 'Expense Breakdown', horizontalalignment='center', verticalalignment='center', fontsize=FONT_SECTION[1], color='gray', transform=ax.transAxes)
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

recent_transaction_category_combobox = None
recent_transaction_category_combobox_window_id = None

def update_recent_transaction_box(event):
    global recent_transaction_category_combobox, recent_transaction_category_combobox_window_id
    recent_transaction_canvas.delete("all")
    current_width = event.width
    current_height = event.height
    draw_rounded_rect(recent_transaction_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR, outline_width=0)
    recent_transaction_canvas.create_text(current_width / 2, current_height / 2, text="₱", font=("Arial", int(current_height * 0.7), "bold"), fill="#f0f0e0", anchor="center", tags="watermark")
    recent_transaction_canvas.tag_lower("watermark")
    recent_transaction_canvas.create_text(20, 20, anchor="nw", text="Recent Expenses", font=FONT_SECTION, fill="black")
    recent_transaction_canvas.create_text(current_width - 30, 20, anchor="ne", text="+", font=("Arial", 28, "bold"), fill="black")
    recent_transaction_canvas.create_text(current_width - 30, 60, anchor="ne", text="Amount", font=FONT_SUBTEXT, fill="black")
    if recent_transaction_category_combobox is None or not recent_transaction_category_combobox.winfo_exists():
        recent_transaction_category_combobox_var = tk.StringVar(value="Category")
        recent_transaction_category_combobox = ttk.Combobox(
            recent_transaction_canvas,
            textvariable=recent_transaction_category_combobox_var,
            values=["Category", "Food", "Travel", "Bills", "Shopping", "Entertainment", "Education", "Health", "Misc."],
            state="readonly",
            width=10,
            font=FONT_SUBTEXT,
            justify="center"
        )
        recent_transaction_category_combobox_window_id = recent_transaction_canvas.create_window(
            70, 60, window=recent_transaction_category_combobox, anchor="w"
        )
    else:
        recent_transaction_canvas.coords(recent_transaction_category_combobox_window_id, 70, 60)
        recent_transaction_canvas.tag_raise(recent_transaction_category_combobox_window_id)
    y_offset = 90
    line_height = 28
    for idx, (category, amount) in enumerate(transactions):
        if y_offset + line_height > current_height - 30:
            break
        recent_transaction_canvas.create_text(30, y_offset, anchor="w", text=f"• {category}", font=FONT_TRANSACTION, fill="black")
        recent_transaction_canvas.create_text(current_width - 30, y_offset, anchor="e", text=f"{amount}", font=FONT_TRANSACTION, fill="black")
        y_offset += line_height

def create_total_expenses_app():
    root = tk.Tk()
    root.title("TrackU - Total Expenses")
    root.state("zoomed")
    root.configure(bg=COLOR_BG)
    root.grid_columnconfigure(0, weight=0, minsize=250)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=0, minsize=85)  # <-- Make navbar taller
    root.grid_rowconfigure(1, weight=1)
    sidebar_frame = tk.Frame(root, bg=COLOR_SIDEBAR, width=250, highlightthickness=0)
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
            logo_label = tk.Label(sidebar_frame, text="TrackU Logo", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR, fg="darkgray")
            logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
    except Exception as e:
        logo_label = tk.Label(sidebar_frame, text="TrackU Logo", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR, fg="darkgray")
        logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
    menu_items = ["", "", "", "Dashboard", "Total Expenses", "Total Savings", "", "", "", "", "", "Profile"]
    sidebar_frame.grid_rowconfigure(len(menu_items) * 2 + 1, weight=1)
    row_idx = 1
    for item in menu_items:
        if item:
            menu_button = tk.Button(sidebar_frame, text=item, font=FONT_MENU, bg=COLOR_SIDEBAR, fg="black",
                                    command=lambda i=item: on_menu_item_click(i, root),
                                    relief="flat",
                                    activebackground=COLOR_NAVBAR,
                                    anchor="w",
                                    padx=15
                                    )
            menu_button.grid(row=row_idx, column=0, pady=5, sticky="ew")
            if item != menu_items[-1] and item != "":
                tk.Frame(sidebar_frame, bg=COLOR_BOX_BORDER, height=1).grid(row=row_idx + 1, column=0, sticky="ew", padx=10)
                row_idx += 1
        row_idx += 1
    sidebar_frame.grid_rowconfigure(row_idx, weight=1)
    global top_right_header_canvas
    top_right_header_canvas = tk.Canvas(root, bg=COLOR_BG, height=85, highlightthickness=0)  # <-- Make navbar taller
    top_right_header_canvas.grid(row=0, column=1, sticky="nsew")
    top_right_header_canvas.bind("<Configure>", draw_top_right_header_content)
    main_content_area = tk.Frame(root, bg=COLOR_BG)
    main_content_area.grid(row=1, column=1, sticky="nsew", padx=30, pady=20)
    main_content_area.grid_columnconfigure(0, weight=1, minsize=300)
    main_content_area.grid_columnconfigure(1, weight=1)
    main_content_area.grid_rowconfigure(0, weight=1)
    pie_chart_section_canvas = tk.Canvas(main_content_area, bg=COLOR_BG, highlightthickness=0)
    pie_chart_section_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=10)
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    month_var = tk.StringVar(value="January")
    month_combo = ttk.Combobox(pie_chart_section_canvas, textvariable=month_var, values=months,
                               state="readonly", font=FONT_SUBTEXT, justify="center", width=10)
    month_combo.current(0)
    total_expenses_amount_lbl = tk.Label(pie_chart_section_canvas, text="Total Expenses:\n₱ 100,000.00",
                                         font=("Georgia", 13), bg=COLOR_BG, fg="black", justify=tk.LEFT)
    pie_chart_section_canvas.bind("<Configure>",
                                  lambda event: update_pie_chart_section(event, pie_chart_section_canvas, month_combo,
                                                                         total_expenses_amount_lbl))
    global recent_transaction_canvas
    recent_transaction_canvas = tk.Canvas(main_content_area, bg=COLOR_BG, highlightthickness=0)
    recent_transaction_canvas.grid(row=0, column=1, sticky="nsew", pady=10)
    global recent_transaction_category_combobox_var, recent_transaction_category_combobox, recent_transaction_category_combobox_window_id
    recent_transaction_category_combobox_var = tk.StringVar(value="Category")
    recent_transaction_category_combobox = ttk.Combobox(
        recent_transaction_canvas,
        textvariable=recent_transaction_category_combobox_var,
        values=["Category", "Food", "Travel", "Bills", "Shopping", "Entertainment", "Education", "Health", "Misc."],
        state="readonly",
        width=10,
        font=FONT_SUBTEXT,
        justify="center"
    )
    recent_transaction_category_combobox_window_id = recent_transaction_canvas.create_window(
        70, 60, window=recent_transaction_category_combobox, anchor="w"
    )
    recent_transaction_canvas.bind("<Configure>", update_recent_transaction_box)
    root.mainloop()

if __name__ == "__main__":
    create_total_expenses_app()