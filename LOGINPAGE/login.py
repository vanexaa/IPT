import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pyglet
import os
import subprocess # Import subprocess to run dashboard.py

# --- Global Font Loading ---
try:
    # Ensure 'Playfair Display.ttf' is in the same directory as this script,
    # or provide a full path to the font file.
    pyglet.font.add_file('Playfair Display.ttf')
except Exception as e:
    # Fallback if font cannot be loaded.
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
CARD_HEIGHT = 550

# --- Helper Functions for Drawing (Login) ---

def draw_rounded_rect_on_card(canvas_obj, x, y, w, h, r, color):
    """Draws the rounded background for the login card on a given canvas."""
    canvas_obj.delete("rounded") # Clear previous drawings
    canvas_obj.create_arc(x, y, x + 2*r, y + 2*r, start=90, extent=90, fill=color, outline=color, tags="rounded")
    canvas_obj.create_arc(x + w - 2*r, y, x + w, y + 2*r, start=0, extent=90, fill=color, outline=color, tags="rounded")
    canvas_obj.create_arc(x, y + h - 2*r, x + 2*r, y + h, start=180, extent=90, fill=color, outline=color, tags="rounded")
    canvas_obj.create_arc(x + w - 2*r, y + h - 2*r, x + w, y + h, start=270, extent=90, fill=color, outline=color, tags="rounded")
    canvas_obj.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color, tags="rounded")
    canvas_obj.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color, tags="rounded")

# --- Login Application ---
def create_login_app():
    """Creates and runs the Tkinter login application window."""
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
        # Check if the image file exists in the same directory as the script
        # Assuming 'testlogo.png' is in the same directory as login.py
        if os.path.exists("testlogo.png"):
            img = Image.open("testlogo.png").resize(LOGO_SIZE, Image.LANCZOS)
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
    rounded_card = tk.Canvas(canvas, width=CARD_WIDTH, height=CARD_HEIGHT, bg=RIGHT_BG, highlightthickness=0)
    card_window = canvas.create_window(0, 0, window=rounded_card) # Initial dummy position

    def center_card(event=None):
        """Centers the login card on the canvas."""
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        # Only center if width and height are positive (i.e., canvas is visible)
        if w > 0 and h > 0:
            canvas.coords(card_window, w // 2, h // 2)

    canvas.bind("<Configure>", center_card) # Bind to canvas resize

    # Draw the initial rounded rectangle
    draw_rounded_rect_on_card(rounded_card, 0, 0, CARD_WIDTH, CARD_HEIGHT, 30, CARD_BG)

    # Frame for login content (placed inside rounded_card canvas)
    card_frame = tk.Frame(rounded_card, width=CARD_WIDTH, height=CARD_HEIGHT, bg=CARD_BG)
    rounded_card.create_window(CARD_WIDTH // 2, CARD_HEIGHT // 2, window=card_frame)

    card_logo_img = None
    try:
        # Assuming 'testlogo.png' is in the same directory as login.py
        if os.path.exists("testlogo.png"):
            card_img = Image.open("testlogo.png").resize(LOGO_SIZE, Image.LANCZOS)
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
        """Handles the login process and launches the dashboard."""
        username = username_var.get()
        if username and username != "Enter Username":
            root.destroy()  # Close the login window
            try:
                # --- OLD CODE ---
                # subprocess.Popen(["python", "dashboard.py"])

                # --- NEW CODE: Adjust path to dashboard.py based on your folder structure ---
                # This path assumes dashboard.py is in a sibling folder named 'DASHBOARD'
                dashboard_path = os.path.join(os.path.dirname(__file__), "..", "DASHBOARD", "dashboard.py")
                subprocess.Popen(["python", dashboard_path])

            except Exception as e:
                messagebox.showerror("Launch Error", f"Failed to launch dashboard.py:\n{e}")
        else:
            messagebox.showerror("Login Error", "Please enter a valid username.")

    login_btn = tk.Button(card_frame, text="LOGIN", font=FONT_BTN, bg=ACCENT, fg="black", width=12, bd=0, relief="flat",
                          command=login, highlightthickness=0)
    login_btn.pack(pady=(10, 30))

    root.mainloop()

if __name__ == "__main__":
    create_login_app()
