import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pyglet
import os

# --- Global Font Loading ---
try:
    pyglet.font.add_file('Playfair Display.ttf')
except Exception as e:
    print(f"Warning: Could not load Playfair Display.ttf. Using default system fonts. Error: {e}")

# --- Colors and Fonts (Shared/Login Specific) ---
LEFT_BG = "#d6e9d5"
RIGHT_BG = "#fdf6e3"
CARD_BG = "#fbe3c0"
ACCENT = "#d6e9d5"
FONT_SUB = ("Playfair Display", 16)
FONT_BTN = ("Playfair Display", 20, "bold")
LOGO_SIZE = (200, 150)
CARD_WIDTH = 500
CARD_HEIGHT = 550

# --- Dashboard Specific Colors and Fonts ---
COLOR_BG = "#fdfdf5"
COLOR_NAVBAR = "#ffe0b2"  # Navbar color
COLOR_SIDEBAR = "#d6e9d5"  # Sidebar color
COLOR_LINE = "#d3d3d3"
COLOR_CANVAS_BAR = "#fdf6e3"
COLOR_BOX_BORDER = "black"
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

# Dummy transaction data for the dashboard
transactions = [
    ("Food", "-100"),
    ("School Supplies", "-100"),
    ("Emergency Funds", "-100"),
    ("School Fees", "-100"),
    ("General Savings", "-100"),
    ("Personal Goal", "-100"),
    ("Future Purchases", "-100")
]


# --- Helper Functions for Drawing (Dashboard) ---

def draw_bottom_rounded_rect(canvas, x, y, w, h, r, color):
    """Draws a rectangle with only bottom corners rounded."""
    canvas.create_rectangle(x, y, x + w, y + r, fill=color, outline=color)
    canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)
    canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x + r, y + h - r, x + w - r, y + h, fill=color, outline=color)


def draw_rounded_rect(canvas, x, y, w, h, r, color):
    """Draws a rectangle with all four corners rounded."""
    canvas.create_arc(x, y, x + 2 * r, y + 2 * r, start=90, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y, x + w, y + 2 * r, start=0, extent=90, fill=color, outline=color)
    canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color)
    canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
    canvas.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color)
    canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)


def create_bar(canvas, heights):
    """Draws bars on a given canvas."""
    canvas.delete("bar")  # Clear existing bars
    bar_width = 30
    spacing = 15
    x = 15
    max_height = 120  # Max bar height
    canvas_height = int(canvas.winfo_height()) if canvas.winfo_height() > 1 else 180
    max_value = max(heights) if heights else 1

    for height in heights:
        h = (height / max_value) * max_height if max_value > 0 else 0
        canvas.create_rectangle(x, canvas_height - h - 10, x + bar_width, canvas_height - 10, fill=BAR_FILL_COLOR,
                                outline="", tags="bar")
        x += bar_width + spacing


# --- Functions to draw/update box content on resize (Dashboard) ---

def update_left_box_canvas(event, box_canvas, month_combobox, title_text, amount_text, bar_canvas):
    """Updates the content of the left spending boxes on resize."""
    box_canvas.delete("all")
    current_width = event.width
    current_height = event.height

    # Draw the main rounded rectangle background
    draw_rounded_rect(box_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR)

    # Position month combobox (centered horizontally, near top)
    box_canvas.create_window(current_width / 2, 40, window=month_combobox, anchor="center")

    # Position amount and title texts (aligned to left)
    box_canvas.create_text(20, 100, text=amount_text, font=FONT_AMOUNT, fill="black", anchor="w")
    box_canvas.create_text(20, 140, text=title_text, font=FONT_SECTION, fill="black", anchor="w")

    # Position bar canvas
    bar_canvas_x = current_width * 0.65
    bar_canvas_y = current_height * 0.55
    box_canvas.create_window(bar_canvas_x, bar_canvas_y, window=bar_canvas)

    # Redraw bars inside the bar_canvas
    create_bar(bar_canvas, [30, 60, 90, 120])


def update_right_canvas(event, right_canvas):
    """Updates the content of the right transactions section on resize."""
    right_canvas.delete("all")
    current_width = event.width
    current_height = event.height

    # Draw the main rounded rectangle background
    draw_rounded_rect(right_canvas, 0, 0, current_width, current_height, 20, COLOR_CANVAS_BAR)

    # Position titles dynamically
    right_canvas.create_text(20, 20, anchor="nw", text="Recent Transaction", font=FONT_SECTION, fill="black")
    right_canvas.create_text(20, 60, anchor="nw", text="Category", font=FONT_SUBTEXT, fill="black")
    right_canvas.create_text(current_width - 30, 60, anchor="ne", text="Amount", font=FONT_SUBTEXT, fill="black")

    # Position transactions dynamically
    y_offset = 100
    line_height = 28
    for idx, (category, amount) in enumerate(transactions):
        right_canvas.create_text(30, y_offset, anchor="w", text=f"• {category}", font=FONT_TRANSACTION, fill="black")
        right_canvas.create_text(current_width - 30, y_offset, anchor="e", text=f"{amount}", font=FONT_TRANSACTION,
                                 fill="black")
        y_offset += line_height

# Function to draw the custom rounded rectangle on the navbar canvas and place content
def draw_navbar_content(event, navbar_canvas):
    """Draws the navbar background and places brand label."""
    navbar_canvas.delete("all")  # Clear previous drawings
    draw_bottom_rounded_rect(navbar_canvas, 0, 0, event.width, event.height, 20, COLOR_NAVBAR)

    # Place the "TrackU" label on the canvas
    brand_label = tk.Label(navbar_canvas, text="TrackU", font=FONT_BRAND, bg=COLOR_NAVBAR, fg="black")
    navbar_canvas.create_window(20, event.height / 2, window=brand_label, anchor="w")


# --- Login Application ---
def create_login_app(on_login_success):
    """Creates and returns the Tkinter login application window."""
    root = tk.Tk()
    root.title("TrackU Login")
    root.state("zoomed")  # Start maximized
    root.geometry("1100x600")
    root.minsize(800, 500)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Left Frame
    left_frame = tk.Frame(root, bg=LEFT_BG)
    left_frame.grid(row=0, column=0, sticky="nsew")
    for i in range(4):
        left_frame.grid_rowconfigure(i, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    # Container for logo + welcome text
    welcome_container = tk.Frame(left_frame, bg=LEFT_BG)
    welcome_container.grid(row=0, column=0, pady=(180, 0), sticky="n")

    # Logo in left panel
    logo_img = None
    try:
        # Check if the image file exists
        if os.path.exists("LOGINPAGE/testlogo.png"):
            img = Image.open("LOGINPAGE/testlogo.png").resize(LOGO_SIZE, Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(img)
            logo = tk.Label(welcome_container, image=logo_img, borderwidth=0, bg=LEFT_BG)
            logo.image = logo_img # Keep a reference!
            logo.pack()
        else:
            # Fallback if image not found
            logo = tk.Label(welcome_container, text="TrackU Logo", font=("Arial", 24, "bold"), bg=LEFT_BG, fg="darkgray")
            logo.pack()
            messagebox.showwarning("Image Warning", "testlogo.png not found. Using placeholder text.")
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load logo image:\n{e}. Using placeholder text.")
        logo = tk.Label(welcome_container, text="TrackU Logo", font=("Arial", 24, "bold"), bg=LEFT_BG, fg="darkgray")
        logo.pack()


    welcome1 = tk.Label(welcome_container, text="Welcome to", font=("Playfair Display", 48, "normal"), bg=LEFT_BG,
                        borderwidth=0)
    welcome1.pack(pady=(10, 0))

    welcome2 = tk.Label(welcome_container, text="TrackU", font=("Playfair Display", 42, "bold"), bg=LEFT_BG)
    welcome2.pack(pady=(0,0))

    tagline = tk.Label(left_frame, text="Track your spending. Save\nsmart. Stress less.", font=FONT_SUB, bg=LEFT_BG, borderwidth=0)
    tagline.grid(row=1, column=0, pady=(0, 0))

    copyright = tk.Label(left_frame, text="© 2025 TrackU. All rights reserved.", font=("Georgia", 12), bg=LEFT_BG)
    copyright.grid(row=3, column=0, pady=(0, 20), sticky="s")

    # Right Frame
    right_frame = tk.Frame(root, bg=RIGHT_BG)
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    # Create canvas once for the grid and card
    canvas = tk.Canvas(right_frame, bg=RIGHT_BG, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    def draw_grid(event=None):
        """Draws a grid on the canvas."""
        canvas.delete("grid_line")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        for i in range(0, w, 30):
            canvas.create_line(i, 0, i, h, fill="#bdbdbd", width=2, tags="grid_line")
        for j in range(0, h, 30):
            canvas.create_line(0, j, w, j, fill="#bdbdbd", width=2, tags="grid_line")
    canvas.bind("<Configure>", draw_grid) # Bind to canvas resize

    # Rounded Card Canvas inside the main canvas
    # Note: rounded_card is a Canvas itself, used to hold the login widgets
    rounded_card = tk.Canvas(canvas, width=CARD_WIDTH, height=CARD_HEIGHT, bg=RIGHT_BG, highlightthickness=0)
    # Use initial positioning, will be updated by center_card
    card_window = canvas.create_window(CARD_WIDTH // 2, CARD_HEIGHT // 2, window=rounded_card)


    def center_card(event=None):
        """Centers the login card on the canvas."""
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        canvas.coords(card_window, w // 2, h // 2)

    canvas.bind("<Configure>", center_card) # Bind to canvas resize

    # Draw rounded rectangle on the rounded_card canvas itself
    def draw_rounded_rect_on_card(x, y, w, h, r, color):
        """Draws the rounded background for the login card."""
        rounded_card.delete("rounded") # Clear previous drawings
        rounded_card.create_arc(x, y, x + 2*r, y + 2*r, start=90, extent=90, fill=color, outline=color, tags="rounded")
        rounded_card.create_arc(x + w - 2*r, y, x + w, y + 2*r, start=0, extent=90, fill=color, outline=color, tags="rounded")
        rounded_card.create_arc(x, y + h - 2*r, x + 2*r, y + h, start=180, extent=90, fill=color, outline=color, tags="rounded")
        rounded_card.create_arc(x + w - 2*r, y + h - 2*r, x + w, y + h, start=270, extent=90, fill=color, outline=color, tags="rounded")
        rounded_card.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color, tags="rounded")
        rounded_card.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color, tags="rounded")

    # Draw the initial rounded rectangle
    draw_rounded_rect_on_card(0, 0, CARD_WIDTH, CARD_HEIGHT, 30, CARD_BG)

    # Frame for login content (placed inside rounded_card canvas)
    card_frame = tk.Frame(rounded_card, width=CARD_WIDTH, height=CARD_HEIGHT, bg=CARD_BG)
    rounded_card.create_window(CARD_WIDTH // 2, CARD_HEIGHT // 2, window=card_frame)

    card_logo_img = None
    try:
        if os.path.exists("LOGINPAGE/testlogo.png"):
            card_img = Image.open("LOGINPAGE/testlogo.png").resize(LOGO_SIZE, Image.LANCZOS)
            card_logo_img = ImageTk.PhotoImage(card_img)
            card_logo = tk.Label(card_frame, image=card_logo_img, bg=CARD_BG, borderwidth=0)
            card_logo.image = card_logo_img # Keep a reference!
            card_logo.pack(pady=(30, 10))
        else:
            card_logo = tk.Label(card_frame, text="TrackU Logo", font=("Arial", 20, "bold"), bg=CARD_BG, fg="darkgray")
            card_logo.pack(pady=(30, 10))
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load card logo image:\n{e}")
        card_logo = tk.Label(card_frame, text="TrackU Logo", font=("Arial", 20, "bold"), bg=CARD_BG, fg="darkgray")
        card_logo.pack(pady=(30, 10))


    card_title = tk.Label(card_frame, text="TrackU", font=("Playfair Display", 28, "bold"), bg=CARD_BG, borderwidth=0)
    card_title.pack(pady=(0, 10))

    username_var = tk.StringVar()
    username_entry = tk.Entry(card_frame, textvariable=username_var, font=("Playfair Display", 18), bd=2, relief="solid",
                              justify="center", fg="grey")
    username_entry.insert(0, "Enter Username")
    username_entry.pack(pady=(5, 10), ipadx=2, ipady=1)

    def on_entry_click(event):
        """Clears placeholder text on entry click."""
        if username_entry.get() == "Enter Username":
            username_entry.delete(0, tk.END)
            username_entry.config(fg='black')

    username_entry.bind("<FocusIn>", on_entry_click)

    def login():
        """Handles the login process and transitions to the dashboard."""
        username = username_var.get()
        if username and username != "Enter Username":
            root.destroy()  # Close the login window
            on_login_success() # Call the callback to open dashboard
        else:
            messagebox.showerror("Login Error", "Please enter a valid username.")

    login_btn = tk.Button(card_frame, text="LOGIN", font=FONT_BTN, bg=ACCENT, fg="black", width=12, bd=0, relief="flat",
                          command=login, highlightthickness=0)
    login_btn.pack(pady=(10, 30))

    return root # Return the root window for external control


# --- Dashboard Application ---
def create_dashboard_app():
    """Creates and runs the Tkinter dashboard application window."""
    root = tk.Tk()
    root.title("TrackU Dashboard")
    root.geometry("950x520")
    root.state("zoomed")
    root.configure(bg=COLOR_BG)

    # --- REVISED ROOT GRID CONFIGURATION ---
    root.grid_columnconfigure(0, weight=0, minsize=250)  # Fixed width for sidebar
    root.grid_columnconfigure(1, weight=1)  # Main content area takes remaining width
    root.grid_rowconfigure(0, weight=0, minsize=65)  # Fixed height for navbar row
    root.grid_rowconfigure(1, weight=1)  # Main content row takes remaining height

    # --- LEFT SIDEBAR FRAME (Spans both rows in column 0) ---
    sidebar_frame = tk.Frame(root, bg=COLOR_SIDEBAR, width=250, highlightthickness=0)
    sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
    sidebar_frame.grid_propagate(False)

    sidebar_frame.grid_columnconfigure(0, weight=1)

    # Define menu_items
    menu_items = ["Dashboard", "Transactions", "Budget", "Reports", "Settings", "", "Profile"] # Added some dummy items
    # This row will take all remaining space, pushing elements to the top
    sidebar_frame.grid_rowconfigure(len(menu_items) * 2, weight=1)

    # Sidebar content
    row_idx = 0
    for item in menu_items:
        if item:
            tk.Label(sidebar_frame, text=item, font=FONT_MENU, bg=COLOR_SIDEBAR, fg="black").grid(row=row_idx, column=0,
                                                                                                  pady=10, sticky="ew")
            # Add separator only if not the last item in the list and not an empty string
            if item != menu_items[-1] and item != "": # Check if not the last item or an empty string for spacing
                tk.Frame(sidebar_frame, bg=COLOR_BOX_BORDER, height=1).grid(row=row_idx + 1, column=0, sticky="ew", padx=10)
                row_idx += 1
        else:
            tk.Label(sidebar_frame, text="", bg=COLOR_SIDEBAR).grid(row=row_idx, column=0, pady=20)
        row_idx += 1

    # --- TOP NAVIGATION BAR (Placed in row 0, column 1) ---
    navbar = tk.Canvas(root, bg=COLOR_BG, height=65, highlightthickness=0)
    navbar.grid(row=0, column=1, sticky="nsew")
    # Bind draw_navbar_content using a lambda to pass the canvas
    navbar.bind("<Configure>", lambda event, c=navbar: draw_navbar_content(event, c))


    # --- MAIN CONTENT FRAME (Placed in row 1, column 1) ---
    main_frame = tk.Frame(root, bg=COLOR_BG)
    main_frame.grid(row=1, column=1, sticky="nsew", padx=(45, 0), pady=10)
    main_frame.grid_columnconfigure(0, weight=1, minsize=1)
    main_frame.grid_columnconfigure(1, weight=3)
    main_frame.grid_rowconfigure(1, weight=1)

    tk.Label(main_frame, text="Welcome, [username]", font=FONT_WELCOME, bg=COLOR_BG).grid(
        row=0, column=0, columnspan=2, sticky="w", padx=(0, 0), pady=(0, 10))

    # Left Section - Spending Boxes (Total Expenses & Total Savings)
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

    # Right Section - Recent Transactions
    right_canvas = tk.Canvas(main_frame, bg=COLOR_BG, highlightthickness=0)
    right_canvas.grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=14)

    # Bind update_right_canvas using a lambda to pass the canvas
    right_canvas.bind("<Configure>", lambda event, c=right_canvas: update_right_canvas(event, c))

    root.mainloop()


# --- Main Application Flow ---
if __name__ == "__main__":
    # This function will be called by the login app upon successful login
    def start_dashboard_after_login():
        create_dashboard_app()

    # Create the login app, passing the function to call on successful login
    login_window = create_login_app(start_dashboard_after_login)
    login_window.mainloop() # Start the login application's main loop
