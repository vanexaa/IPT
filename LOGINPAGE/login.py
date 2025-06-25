import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pyglet
import os
import subprocess
import sys

# No longer explicitly importing sqlite3 here as database_manager abstracts it

# --- Path setup for database_manager.py ---
# Get the directory of the current script (login.py is in LOGINPAGE/)
current_script_dir = os.path.dirname(__file__)

# Go up one level (from LOGINPAGE/ to the project root, e.g., 'NEW_IPT/')
# Then go into 'TOTAL EXPENSES' where database_manager.py is
database_folder_path = os.path.abspath(os.path.join(current_script_dir, "..", "TOTAL EXPENSES"))

# Add this path to sys.path
if database_folder_path not in sys.path:
    sys.path.append(database_folder_path)
# ------------------------------------------

# IMPORTANT: Import the database_manager module after sys.path setup
import database_manager

# --- Global Font Loading ---
try:
    # This path assumes Playfair Display.ttf is in the same directory as login.py
    pyglet.font.add_file('Playfair Display.ttf')
except Exception as e:
    print(f"Warning: Could not load Playfair Display.ttf. Using default system fonts. Error: {e}")

# --- Colors and Fonts ---
LEFT_BG = "#d6e9d5"
RIGHT_BG = "#fdf6e3"
CARD_BG = "#fbe3c0"
ACCENT = "#d6e9d5"
FONT_SUB = ("Playfair Display", 16)
FONT_BTN = ("Playfair Display", 20, "bold")
LOGO_SIZE = (200, 150)
CARD_WIDTH = 500
CARD_HEIGHT = 450  # Adjusted height to accommodate single entry and buttons

# Global reference for the root window
root_window = None


def draw_rounded_rect_on_card(canvas_obj, x, y, w, h, r, color):
    canvas_obj.delete("rounded")
    canvas_obj.create_arc(x, y, x + 2 * r, y + 2 * r, start=90, extent=90, fill=color, outline=color, tags="rounded")
    canvas_obj.create_arc(x + w - 2 * r, y, x + w, y + 2 * r, start=0, extent=90, fill=color, outline=color,
                          tags="rounded")
    canvas_obj.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color,
                          tags="rounded")
    canvas_obj.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color,
                          tags="rounded")
    canvas_obj.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color, tags="rounded")
    canvas_obj.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color, tags="rounded")


def create_rounded_entry(parent, width, height, radius, bg_color, entry_var, font, fg, placeholder, show_char=None):
    entry_canvas = tk.Canvas(parent, width=width, height=height, bg=bg_color, highlightthickness=0)
    # Draw rounded rectangle
    entry_canvas.create_arc((0, 0, 2 * radius, 2 * radius), start=90, extent=90, fill="white", outline="white")
    entry_canvas.create_arc((width - 2 * radius, 0, width, 2 * radius), start=0, extent=90, fill="white",
                            outline="white")
    entry_canvas.create_arc((0, height - 2 * radius, 2 * radius, height), start=180, extent=90, fill="white",
                            outline="white")
    entry_canvas.create_arc((width - 2 * radius, height - 2 * radius, width, height), start=270, extent=90,
                            fill="white", outline="white")
    entry_canvas.create_rectangle((radius, 0, width - radius, height), fill="white", outline="white")
    entry_canvas.create_rectangle((0, radius, width, height - radius), fill="white", outline="white")
    # Place Entry widget
    entry = tk.Entry(entry_canvas, textvariable=entry_var, font=font, bd=0, relief="flat", justify="center", fg=fg,
                     bg="white", show=show_char)
    # entry.insert(0, placeholder) # We will insert placeholder in the main function to control initial state
    entry_canvas.create_window(width // 2, height // 2, window=entry, width=width - 16, height=height - 10)
    return entry_canvas, entry


def create_rounded_button(parent, width, height, radius, bg_color, text, font, fg, command):
    btn_canvas = tk.Canvas(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
    # Draw rounded rectangle
    btn_canvas.create_arc((0, 0, 2 * radius, 2 * radius), start=90, extent=90, fill=bg_color, outline=bg_color)
    btn_canvas.create_arc((width - 2 * radius, 0, width, 2 * radius), start=0, extent=90, fill=bg_color,
                          outline=bg_color)
    btn_canvas.create_arc((0, height - 2 * radius, 2 * radius, height), start=180, extent=90, fill=bg_color,
                          outline=bg_color)
    btn_canvas.create_arc((width - 2 * radius, height - 2 * radius, width, height), start=270, extent=90, fill=bg_color,
                          outline=bg_color)
    btn_canvas.create_rectangle((radius, 0, width - radius, height), fill=bg_color, outline=bg_color)
    btn_canvas.create_rectangle((0, radius, width, height - radius), fill=bg_color, outline=bg_color)
    # Place text
    btn_text = btn_canvas.create_text(width // 2, height // 2, text=text, font=font, fill=fg)

    # Bind click
    def on_click(event):
        command()

    btn_canvas.bind("<Button-1>", on_click)
    btn_canvas.config(cursor="hand2")
    return btn_canvas


def launch_dashboard(user_id):
    """Launches the dashboard.py script, passing the user_id as an argument."""
    global root_window

    # Close the login window first
    if root_window and root_window.winfo_exists():
        root_window.destroy()

    try:
        dashboard_path = os.path.abspath(os.path.join(current_script_dir, "..", "DASHBOARD", "dashboard.py"))

        # Prepare command with Python executable and script path, plus the user_id argument
        cmd = [sys.executable, dashboard_path, str(user_id)]

        if sys.platform.startswith('win'):
            subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(cmd)  # For Linux/macOS

        print(f"Launched dashboard.py for user ID: {user_id}")
    except FileNotFoundError:
        messagebox.showerror("Launch Error", "Python interpreter or dashboard.py not found. Ensure paths are correct.")
    except Exception as e:
        messagebox.showerror("Launch Error", f"Failed to launch dashboard.py:\n{e}")


def login_or_register(username_var, username_placeholder):
    """Handles the login or registration process."""
    username = username_var.get().strip()  # Get and strip whitespace

    if username == username_placeholder or not username:
        messagebox.showerror("Login/Registration Error", "Please enter a username.")
        return

    user_id = database_manager.get_user_id(username)  # Check if user exists

    if user_id is not None:  # User exists
        messagebox.showinfo("Login Success", f"Welcome back, {username}!")
        launch_dashboard(user_id)
    else:  # User does not exist, attempt to register
        if database_manager.add_user(username):
            user_id = database_manager.get_user_id(username)  # Get the newly created user_id
            if user_id is not None:
                messagebox.showinfo("Registration & Login Success",
                                    f"Welcome, {username}! Your account has been created.")
                launch_dashboard(user_id)
            else:
                # This case should ideally not happen if add_user returns True, but handle defensively
                messagebox.showerror("Error",
                                     "Account created but could not retrieve user ID. Please try logging in again.")
        else:
            # add_user returned False, likely due to IntegrityError (username already exists from another process)
            messagebox.showerror("Error", f"Could not create account for '{username}'. It might already exist.")


def create_login_app():
    global root_window
    root_window = tk.Tk()
    root_window.title("TrackU Login")
    root_window.state("zoomed")
    root_window.geometry("1100x600")
    root_window.minsize(800, 500)

    # Initialize the database when the application starts
    # This will now create the 'users' table as well, thanks to database_manager.py update
    database_manager.initialize_db()

    root_window.grid_rowconfigure(0, weight=1)
    root_window.grid_columnconfigure(0, weight=1, minsize=100)
    root_window.grid_columnconfigure(1, weight=3)

    # Left Frame
    left_frame = tk.Frame(root_window, bg=LEFT_BG)
    left_frame.grid(row=0, column=0, sticky="nsew")
    for i in range(4):
        left_frame.grid_rowconfigure(i, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    welcome_container = tk.Frame(left_frame, bg=LEFT_BG)
    welcome_container.grid(row=0, column=0, pady=(180, 0), sticky="n")

    global sidebar_logo_img  # Keep reference
    sidebar_logo_img = None
    try:
        # Assuming testlogo.png is in the same directory as login.py
        if os.path.exists("testlogo.png"):
            img = Image.open("testlogo.png").resize(LOGO_SIZE, Image.LANCZOS)
            sidebar_logo_img = ImageTk.PhotoImage(img)
            logo = tk.Label(welcome_container, image=sidebar_logo_img, borderwidth=0, bg=LEFT_BG)
            logo.image = sidebar_logo_img
            logo.pack()
        else:
            logo = tk.Label(welcome_container, text="TrackU Logo", font=("Arial", 24, "bold"), bg=LEFT_BG,
                            fg="darkgray")
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
    welcome2.pack(pady=(0, 0))

    tagline = tk.Label(left_frame, text="Track your spending. Save\nsmart. Stress less.", font=FONT_SUB, bg=LEFT_BG,
                       borderwidth=0)
    tagline.grid(row=1, column=0, pady=(0, 0))

    copyright_label = tk.Label(left_frame, text="© 2025 TrackU. All rights reserved.", font=("Georgia", 12), bg=LEFT_BG)
    copyright_label.grid(row=3, column=0, pady=(0, 20), sticky="s")

    # Right Frame
    right_frame = tk.Frame(root_window, bg=RIGHT_BG)
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    canvas = tk.Canvas(right_frame, bg=RIGHT_BG, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    global CARD_HEIGHT
    rounded_card = tk.Canvas(canvas, width=CARD_WIDTH, height=CARD_HEIGHT, bg=RIGHT_BG, highlightthickness=0)
    card_window = canvas.create_window(0, 0, window=rounded_card, tags="login_card_window")

    def draw_grid():
        canvas.delete("grid_line")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        for i in range(0, w, 30):
            canvas.create_line(i, 0, i, h, fill="#808080", width=1, tags="grid_line")
        for j in range(0, h, 30):
            canvas.create_line(0, j, w, j, fill="#808080", width=1, tags="grid_line")
        canvas.tag_raise("login_card_window")

    def center_card(event=None):
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w > 0 and h > 0:
            canvas.coords(card_window, w // 2, h // 2)
            canvas.tag_raise("login_card_window")
        # draw_grid() # Commented out, only for development

    canvas.bind("<Configure>", center_card)

    draw_rounded_rect_on_card(rounded_card, 0, 0, CARD_WIDTH, CARD_HEIGHT, 30, CARD_BG)

    card_frame = tk.Frame(rounded_card, width=CARD_WIDTH, height=CARD_HEIGHT, bg=CARD_BG)
    rounded_card.create_window(CARD_WIDTH // 2, CARD_HEIGHT // 2, window=card_frame)

    card_logo_img = None  # Needs to be global or held as a reference by a widget
    try:
        # Assuming testlogo.png is in the same directory as login.py
        if os.path.exists("testlogo.png"):
            img = Image.open("testlogo.png").resize(LOGO_SIZE, Image.LANCZOS)
            card_logo_img = ImageTk.PhotoImage(img)
            card_logo = tk.Label(card_frame, image=card_logo_img, bg=CARD_BG, borderwidth=0)
            card_logo.image = card_logo_img  # Keep a reference!
            card_logo.pack(pady=(30, 10))
        else:
            card_logo = tk.Label(card_frame, text="TrackU Logo", font=("Arial", 20, "bold"), bg=CARD_BG, fg="darkgray")
            card_logo.pack(pady=(30, 10))
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load card logo image:\n{e}")
        card_logo = tk.Label(card_frame, text="TrackU Logo", font=("Arial", 20, "bold"), bg=CARD_BG, fg="darkgray")
        card_logo.pack(pady=(30, 10))

    card_title = tk.Label(card_frame, text="TrackU", font=("Playfair Display", 28, "bold"), bg=CARD_BG, borderwidth=0)
    card_title.pack(pady=(0, 20))

    username_var = tk.StringVar()
    username_placeholder = "Enter Username"
    rounded_entry_canvas_user, username_entry = create_rounded_entry(
        card_frame, width=340, height=48, radius=24, bg_color=CARD_BG,
        entry_var=username_var, font=("Playfair Display", 18), fg="grey", placeholder=username_placeholder
    )
    # Insert placeholder after creation of entry widget
    username_entry.insert(0, username_placeholder)
    username_entry.config(fg='grey')

    rounded_entry_canvas_user.pack(pady=(5, 30))

    def on_username_entry_click(event):
        # Only clear if the current text is the placeholder
        if username_entry.get() == username_placeholder:
            username_entry.delete(0, tk.END)
            username_entry.config(fg='black')

    username_entry.bind("<FocusIn>", on_username_entry_click)

    # Add a focus out event to put placeholder back if empty
    def on_username_entry_focusout(event):
        if not username_entry.get():
            username_entry.insert(0, username_placeholder)
            username_entry.config(fg='grey')

    username_entry.bind("<FocusOut>", on_username_entry_focusout)

    rounded_login_register_btn = create_rounded_button(
        card_frame, width=220, height=40, radius=19, bg_color=ACCENT,
        text="LOGIN", font=("Playfair Display", 14, "bold"), fg="black",
        command=lambda: login_or_register(username_var, username_placeholder)  # Pass username_var and placeholder
    )
    rounded_login_register_btn.pack(pady=(10, 30))

    root_window.mainloop()


if __name__ == "__main__":
    create_login_app()
