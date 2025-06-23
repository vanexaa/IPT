import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pyglet
import os
import subprocess
import sqlite3 # Import sqlite3 for potential error handling, though database_manager abstracts most of it

# --- Import database_manager functions ---
import sys

# --- Path setup for database_manager.py ---
# Get the directory of the current script (login.py is in LOGINPAGE/)
current_script_dir = os.path.dirname(__file__)

# Go up one level (from LOGINPAGE/ to NEW_IPT/)
# Then go into 'TOTAL EXPENSES' where database_manager.py is
database_folder_path = os.path.abspath(os.path.join(current_script_dir, "..", "TOTAL EXPENSES"))

# Add this path to sys.path
if database_folder_path not in sys.path:
    sys.path.append(database_folder_path)
# ------------------------------------------

# IMPORTANT: Explicitly import functions from database_manager
# get_user_id will be used to check existence and add_user for 'registration'
from database_manager import initialize_db, connect_db, add_user, get_user_id

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
# Reduced height as password field is removed
CARD_HEIGHT = 450 # Adjusted height to accommodate single entry and buttons

def draw_rounded_rect_on_card(canvas_obj, x, y, w, h, r, color):
    canvas_obj.delete("rounded")
    canvas_obj.create_arc(x, y, x + 2 * r, y + 2 * r, start=90, extent=90, fill=color, outline=color, tags="rounded")
    canvas_obj.create_arc(x + w - 2 * r, y, x + w, y + 2 * r, start=0, extent=90, fill=color, outline=color, tags="rounded")
    canvas_obj.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, fill=color, outline=color, tags="rounded")
    canvas_obj.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, fill=color, outline=color, tags="rounded")
    canvas_obj.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color, tags="rounded")
    canvas_obj.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color, tags="rounded")

def create_rounded_entry(parent, width, height, radius, bg_color, entry_var, font, fg, placeholder, show_char=None):
    entry_canvas = tk.Canvas(parent, width=width, height=height, bg=bg_color, highlightthickness=0)
    # Draw rounded rectangle
    entry_canvas.create_arc((0, 0, 2*radius, 2*radius), start=90, extent=90, fill="white", outline="white")
    entry_canvas.create_arc((width-2*radius, 0, width, 2*radius), start=0, extent=90, fill="white", outline="white")
    entry_canvas.create_arc((0, height-2*radius, 2*radius, height), start=180, extent=90, fill="white", outline="white")
    entry_canvas.create_arc((width-2*radius, height-2*radius, width, height), start=270, extent=90, fill="white", outline="white")
    entry_canvas.create_rectangle((radius, 0, width-radius, height), fill="white", outline="white")
    entry_canvas.create_rectangle((0, radius, width, height-radius), fill="white", outline="white")
    # Place Entry widget
    entry = tk.Entry(entry_canvas, textvariable=entry_var, font=font, bd=0, relief="flat", justify="center", fg=fg, bg="white", show=show_char)
    entry.insert(0, placeholder)
    entry_window = entry_canvas.create_window(width//2, height//2, window=entry, width=width-16, height=height-10)
    return entry_canvas, entry

def create_rounded_button(parent, width, height, radius, bg_color, text, font, fg, command):
    btn_canvas = tk.Canvas(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)
    # Draw rounded rectangle
    btn_canvas.create_arc((0, 0, 2*radius, 2*radius), start=90, extent=90, fill=bg_color, outline=bg_color)
    btn_canvas.create_arc((width-2*radius, 0, width, 2*radius), start=0, extent=90, fill=bg_color, outline=bg_color)
    btn_canvas.create_arc((0, height-2*radius, 2*radius, height), start=180, extent=90, fill=bg_color, outline=bg_color)
    btn_canvas.create_arc((width-2*radius, height-2*radius, width, height), start=270, extent=90, fill=bg_color, outline=bg_color)
    btn_canvas.create_rectangle((radius, 0, width-radius, height), fill=bg_color, outline=bg_color)
    btn_canvas.create_rectangle((0, radius, width, height-radius), fill=bg_color, outline=bg_color)
    # Place text
    btn_text = btn_canvas.create_text(width//2, height//2, text=text, font=font, fill=fg)
    # Bind click
    def on_click(event):
        command()
    btn_canvas.bind("<Button-1>", on_click)
    btn_canvas.config(cursor="hand2")
    return btn_canvas

def create_login_app():
    root = tk.Tk()
    root.title("TrackU Login")
    root.state("zoomed")
    root.geometry("1100x600")
    root.minsize(800, 500)

    # Initialize the database when the application starts
    initialize_db() # Now directly callable

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1, minsize=100)
    root.grid_columnconfigure(1, weight=3)

    # Left Frame
    left_frame = tk.Frame(root, bg=LEFT_BG)
    left_frame.grid(row=0, column=0, sticky="nsew")
    for i in range(4):
        left_frame.grid_rowconfigure(i, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    welcome_container = tk.Frame(left_frame, bg=LEFT_BG)
    welcome_container.grid(row=0, column=0, pady=(180, 0), sticky="n")

    logo_img = None
    try:
        # Assuming testlogo.png is in the same directory as login.py
        if os.path.exists("testlogo.png"):
            img = Image.open("testlogo.png").resize(LOGO_SIZE, Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(img)
            logo = tk.Label(welcome_container, image=logo_img, borderwidth=0, bg=LEFT_BG)
            logo.image = logo_img
            logo.pack()
        else:
            logo = tk.Label(welcome_container, text="TrackU Logo", font=("Arial", 24, "bold"), bg=LEFT_BG, fg="darkgray")
            logo.pack()
            messagebox.showwarning("Image Warning", "testlogo.png not found. Using placeholder text.")
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load logo image:\n{e}. Using placeholder text.")
        logo = tk.Label(welcome_container, text="TrackU Logo", font=("Arial", 24, "bold"), bg=LEFT_BG, fg="darkgray")
        logo.pack()

    welcome1 = tk.Label(welcome_container, text="Welcome to", font=("Playfair Display", 48, "normal"), bg=LEFT_BG, borderwidth=0)
    welcome1.pack(pady=(10, 0))

    welcome2 = tk.Label(welcome_container, text="TrackU", font=("Playfair Display", 42, "bold"), bg=LEFT_BG)
    welcome2.pack(pady=(0, 0))

    tagline = tk.Label(left_frame, text="Track your spending. Save\nsmart. Stress less.", font=FONT_SUB, bg=LEFT_BG, borderwidth=0)
    tagline.grid(row=1, column=0, pady=(0, 0))

    copyright = tk.Label(left_frame, text="© 2025 TrackU. All rights reserved.", font=("Georgia", 12), bg=LEFT_BG)
    copyright.grid(row=3, column=0, pady=(0, 20), sticky="s")

    # Right Frame
    right_frame = tk.Frame(root, bg=RIGHT_BG)
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    canvas = tk.Canvas(right_frame, bg=RIGHT_BG, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    global CARD_HEIGHT # Use the adjusted CARD_HEIGHT
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
        draw_grid()

    canvas.bind("<Configure>", center_card)

    draw_rounded_rect_on_card(rounded_card, 0, 0, CARD_WIDTH, CARD_HEIGHT, 30, CARD_BG)

    card_frame = tk.Frame(rounded_card, width=CARD_WIDTH, height=CARD_HEIGHT, bg=CARD_BG)
    rounded_card.create_window(CARD_WIDTH // 2, CARD_HEIGHT // 2, window=card_frame)

    card_logo_img = None
    try:
        if os.path.exists("testlogo.png"):
            img = Image.open("testlogo.png").resize(LOGO_SIZE, Image.LANCZOS)
            card_logo_img = ImageTk.PhotoImage(img)
            card_logo = tk.Label(card_frame, image=card_logo_img, bg=CARD_BG, borderwidth=0)
            card_logo.image = card_logo_img
            card_logo.pack(pady=(30, 10))
        else:
            card_logo = tk.Label(card_frame, text="TrackU Logo", font=("Arial", 20, "bold"), bg=CARD_BG, fg="darkgray")
            card_logo.pack(pady=(30, 10))
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load card logo image:\n{e}")
        card_logo = tk.Label(card_frame, text="TrackU Logo", font=("Arial", 20, "bold"), bg=CARD_BG, fg="darkgray")
        card_logo.pack(pady=(30, 10))

    card_title = tk.Label(card_frame, text="TrackU", font=("Playfair Display", 28, "bold"), bg=CARD_BG, borderwidth=0)
    card_title.pack(pady=(0, 20)) # Adjusted padding

    username_var = tk.StringVar()
    username_placeholder = "Enter Username"
    rounded_entry_canvas_user, username_entry = create_rounded_entry(
        card_frame, width=340, height=48, radius=24, bg_color=CARD_BG,
        entry_var=username_var, font=("Playfair Display", 18), fg="grey", placeholder=username_placeholder
    )
    rounded_entry_canvas_user.pack(pady=(5, 30)) # Adjusted padding, only one entry field

    def on_username_entry_click(event):
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


    def login_or_register():
        username = username_var.get().strip() # Get and strip whitespace

        if username == username_placeholder or not username:
            messagebox.showerror("Login/Registration Error", "Please enter a username.")
            return

        user_id = get_user_id(username) # Check if user exists

        if user_id:
            # User exists, proceed with login
            messagebox.showinfo("Login Success", f"Welcome back, {username}!")
            root.destroy()
            try:
                # Pass the user_id as a command-line argument to dashboard.py
                dashboard_path = os.path.abspath(os.path.join(current_script_dir, "..", "DASHBOARD", "dashboard.py"))
                subprocess.Popen(["python", dashboard_path, str(user_id)])
            except Exception as e:
                messagebox.showerror("Launch Error", f"Failed to launch dashboard.py:\n{e}")
        else:
            # User does not exist, register them
            if add_user(username): # Call add_user without password
                user_id = get_user_id(username) # Get the newly created user_id
                messagebox.showinfo("Registration & Login Success", f"Welcome, {username}! Your account has been created.")
                root.destroy()
                try:
                    dashboard_path = os.path.abspath(os.path.join(current_script_dir, "..", "DASHBOARD", "dashboard.py"))
                    subprocess.Popen(["python", dashboard_path, str(user_id)])
                except Exception as e:
                    messagebox.showerror("Launch Error", f"Failed to launch dashboard.py:\n{e}")
            else:
                messagebox.showerror("Error", f"Could not create account for '{username}'. Please try again.")


    rounded_login_register_btn = create_rounded_button(
        card_frame, width=220, height=40, radius=19, bg_color=ACCENT,
        text="LOGIN", font=("Playfair Display", 14, "bold"), fg="black", command=login_or_register
    )
    rounded_login_register_btn.pack(pady=(10, 30)) # Adjusted padding, single button

    root.mainloop()

if __name__ == "__main__":
    create_login_app()