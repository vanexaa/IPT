import tkinter as tk
from tkinter import ttk, messagebox
import pyglet
from PIL import Image, ImageTk
import os
import subprocess
import sys

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

BAR_COLOR = "#fdf6e3"
BAR_FILL_COLOR = "#ffa726"

LOGO_SIZE_SIDEBAR = (150, 100)

transactions = [
    ("Food", "-100"),
    ("School Supplies", "-100"),
    ("Emergency Funds", "-100"),
    ("School Fees", "-100"),
    ("General Savings", "-100"),
    ("Personal Goal", "-100"),
    ("Future Purchases", "-100")
]

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

def create_bar(canvas, heights):
    canvas.delete("bar")
    bar_width = 30
    spacing = 15
    x = 15
    max_height = 120
    canvas_height = int(canvas.winfo_height()) if canvas.winfo_height() > 1 else 180
    max_value = max(heights) if heights else 1
    for height in heights:
        h = (height / max_value) * max_height if max_value > 0 else 0
        canvas.create_rectangle(x, canvas_height - h - 10, x + bar_width, canvas_height - 10, fill=BAR_FILL_COLOR,
                                outline="", tags="bar")
        x += bar_width + spacing

def update_left_box_canvas(event, box_canvas, month_combobox, title_text, amount_text, bar_canvas):
    box_canvas.delete("all")
    current_width = event.width
    current_height = event.height
    draw_rounded_rect(box_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR)
    box_canvas.create_window(current_width / 2, 40, window=month_combobox, anchor="center")
    box_canvas.create_text(20, 100, text=amount_text, font=FONT_AMOUNT, fill="black", anchor="w")
    box_canvas.create_text(20, 140, text=title_text, font=FONT_SECTION, fill="black", anchor="w")
    bar_canvas_x_pos = current_width * 0.65
    bar_canvas_y_pos = current_height * 0.55
    box_canvas.create_window(bar_canvas_x_pos, bar_canvas_y_pos, window=bar_canvas, anchor="center")
    bar_canvas.config(width=160, height=180)
    create_bar(bar_canvas, [30, 60, 90, 120])

def update_right_canvas(event, right_canvas_obj):
    right_canvas_obj.delete("all")
    current_width = event.width
    current_height = event.height
    draw_rounded_rect(right_canvas_obj, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR)
    right_canvas_obj.create_text(20, 20, anchor="nw", text="Recent Transaction", font=FONT_SECTION, fill="black")
    right_canvas_obj.create_text(20, 60, anchor="nw", text="Category", font=FONT_SUBTEXT, fill="black")
    right_canvas_obj.create_text(current_width - 30, 60, anchor="ne", text="Amount", font=FONT_SUBTEXT, fill="black")
    y_offset = 100
    line_height = 28
    for idx, (category, amount) in enumerate(transactions):
        right_canvas_obj.create_text(30, y_offset, anchor="w", text=f"• {category}", font=FONT_TRANSACTION,
                                     fill="black")
        right_canvas_obj.create_text(current_width - 30, y_offset, anchor="e", text=f"{amount}", font=FONT_TRANSACTION,
                                     fill="black")
        y_offset += line_height

def draw_navbar_content(event, navbar_canvas_obj):
    navbar_canvas_obj.delete("all")
    draw_bottom_rounded_rect(navbar_canvas_obj, 0, 0, event.width, event.height, 20, COLOR_NAVBAR)
    brand_label = tk.Label(navbar_canvas_obj, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
    navbar_canvas_obj.create_window(20, event.height / 2, window=brand_label, anchor="w")

def on_menu_item_click(item_name, current_root):
    print(f"'{item_name}' was clicked!")
    current_dashboard_dir = os.path.dirname(__file__)
    script_to_launch = None

    if item_name == "Dashboard":
        script_to_launch = os.path.join(current_dashboard_dir, "dashboard.py")
    elif item_name == "Total Expenses":
        script_to_launch = os.path.join(current_dashboard_dir, "..", "TOTAL EXPENSES", "expenses.py")
    elif item_name == "Total Savings":
        script_to_launch = os.path.join(current_dashboard_dir, "..", "TOTAL SAVINGS", "savings.py")
    elif item_name == "Profile":
        print("Profile button clicked. (No specific script to launch yet)")
        return

    if script_to_launch:
        try:
            subprocess.Popen(
                [sys.executable, script_to_launch],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            print(f"Launched: {script_to_launch}")
        except FileNotFoundError:
            messagebox.showerror("Launch Error", "Python interpreter not found. Ensure Python is in your PATH.")
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch {script_to_launch}:\n{e}")
    current_root.destroy()

def create_dashboard_app():
    root = tk.Tk()
    root.title("TrackU Dashboard")
    root.geometry("950x520")
    root.state("zoomed")
    root.configure(bg=COLOR_BG)

    root.grid_columnconfigure(0, weight=0, minsize=320)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=0, minsize=100)
    root.grid_rowconfigure(1, weight=1)

    sidebar_frame = tk.Frame(root, bg=COLOR_SIDEBAR, width=150, highlightthickness=0)
    sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
    sidebar_frame.grid_propagate(False)
    sidebar_frame.grid_columnconfigure(0, weight=1)

    global sidebar_logo_img
    sidebar_logo_img = None
    try:
        if os.path.exists("testlogo.png"):
            img = Image.open("testlogo.png").resize(LOGO_SIZE_SIDEBAR, Image.LANCZOS)
            sidebar_logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(sidebar_frame, image=sidebar_logo_img, bg=COLOR_SIDEBAR, borderwidth=0)
            logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
        else:
            logo_label = tk.Label(sidebar_frame, text="TrackU Logo", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR, fg="darkgray")
            logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")
            print("Warning: testlogo.png not found in dashboard directory. Using placeholder text.")
    except Exception as e:
        print(f"Error loading sidebar logo: {e}. Using placeholder text.")
        logo_label = tk.Label(sidebar_frame, text="TrackU Logo", font=("Arial", 16, "bold"), bg=COLOR_SIDEBAR, fg="darkgray")
        logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")

    menu_items = ["", "", "Dashboard", "Total Expenses", "Total Savings", "", "", "", "", "", "Profile"]
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
                tk.Frame(sidebar_frame, bg=COLOR_BOX_BORDER, height=1).grid(row=row_idx + 1, column=0, sticky="ew",
                                                                            padx=10)
                row_idx += 1
        else:
            tk.Label(sidebar_frame, text="", bg=COLOR_SIDEBAR).grid(row=row_idx, column=0, pady=10)
        row_idx += 1

    navbar = tk.Canvas(root, bg=COLOR_BG, height=65, highlightthickness=0)
    navbar.grid(row=0, column=1, sticky="nsew")
    navbar.bind("<Configure>", lambda event, c=navbar: draw_navbar_content(event, c))

    main_frame = tk.Frame(root, bg=COLOR_BG)
    main_frame.grid(row=1, column=1, sticky="nsew", padx=(45, 0), pady=10)
    main_frame.grid_columnconfigure(0, weight=1, minsize=1)
    main_frame.grid_columnconfigure(1, weight=3)
    main_frame.grid_rowconfigure(1, weight=1)

    tk.Label(main_frame, text="Welcome, [username]", font=FONT_WELCOME, bg=COLOR_BG).grid(
        row=0, column=0, columnspan=2, sticky="w", padx=(0, 0), pady=(0, 10))

    left_frame = tk.Frame(main_frame, bg=COLOR_BG)
    left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 0))
    left_frame.grid_rowconfigure((0, 1), weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    box_titles = ["Total Expenses", "Total Savings"]
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    month_comboboxes = []
    bar_canvases = []

    for i in range(2):
        box_canvas = tk.Canvas(left_frame, bg=COLOR_BG, highlightthickness=0)
        box_canvas.grid(row=i, column=0, pady=15, sticky="nsew")

        month_combobox = ttk.Combobox(box_canvas, values=months, state="readonly", width=15, font=FONT_SUBTEXT,
                                      justify="center")
        month_combobox.current(0)
        month_comboboxes.append(month_combobox)

        bar_canvas_child = tk.Canvas(box_canvas, width=160, height=180, bg=COLOR_CANVAS_BAR, highlightthickness=0)
        bar_canvases.append(bar_canvas_child)

        box_canvas.bind("<Configure>", lambda event, bc=box_canvas, mc=month_combobox, bt=box_titles[i], at="₱ 0.00",
                                              brc=bar_canvas_child: update_left_box_canvas(event, bc, mc, bt, at, brc))

    right_canvas = tk.Canvas(main_frame, bg=COLOR_BG, highlightthickness=0)
    right_canvas.grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=14)
    right_canvas.bind("<Configure>", lambda event, c=right_canvas: update_right_canvas(event, c))

    root.mainloop()

if __name__ == "__main__":
    create_dashboard_app()