import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pyglet
import os
import subprocess

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
FONT_BTN = ("Playfair Display", 20, "bold") # Changed to match global definition
LOGO_SIZE = (200, 150)
CARD_WIDTH = 500
CARD_HEIGHT = 550

# --- Helper Functions for Drawing ---

def draw_rounded_rect_on_canvas(canvas_obj, x, y, w, h, r, color, tags=None):
    """Draws a rounded rectangle on a given canvas.
       If tags is provided, it will replace existing tags."""
    if tags:
        canvas_obj.delete(tags) # Clear previous drawings with these tags

    # Draw rounded corners
    canvas_obj.create_arc(x, y, x + 2*r, y + 2*r, start=90, extent=90, fill=color, outline=color, tags=tags)
    canvas_obj.create_arc(x + w - 2*r, y, x + w, y + 2*r, start=0, extent=90, fill=color, outline=color, tags=tags)
    canvas_obj.create_arc(x, y + h - 2*r, x + 2*r, y + h, start=180, extent=90, fill=color, outline=color, tags=tags)
    canvas_obj.create_arc(x + w - 2*r, y + h - 2*r, x + w, y + h, start=270, extent=90, fill=color, outline=color, tags=tags)
    # Draw straight sections
    canvas_obj.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color, tags=tags)
    canvas_obj.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color, tags=tags)


def create_rounded_button(parent, width, height, radius, bg_color, text, font, fg, command):
    """Creates a custom rounded button using a Canvas."""
    btn_canvas = tk.Canvas(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0)

    # Draw the rounded rectangle for the button
    draw_rounded_rect_on_canvas(btn_canvas, 0, 0, width, height, radius, bg_color)

    # Create the text for the button
    btn_text = btn_canvas.create_text(width//2, height//2, text=text, font=font, fill=fg)

    # Bind click event to the canvas
    def on_click(event):
        command()
    btn_canvas.bind("<Button-1>", on_click)
    btn_canvas.config(cursor="hand2") # Change cursor on hover
    return btn_canvas

# --- Login Application ---
def create_login_app():
    """Creates and runs the Tkinter login application window."""
    root = tk.Tk()
    root.title("TrackU Login")
    root.state("zoomed")  # Start maximized
    root.geometry("1100x600")
    root.minsize(800, 500)

    # Configure grid weights for responsive layout
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1, minsize=100)
    root.grid_columnconfigure(1, weight=3)

    # --- Left Frame (Welcome & Branding) ---
    left_frame = tk.Frame(root, bg=LEFT_BG)
    left_frame.grid(row=0, column=0, sticky="nsew")
    for i in range(4):
        left_frame.grid_rowconfigure(i, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    # Container for logo + welcome text (to center them vertically within their row)
    welcome_container = tk.Frame(left_frame, bg=LEFT_BG)
    welcome_container.grid(row=0, column=0, pady=(180, 0), sticky="n") # Anchor to top

    # Logo in left panel
    logo_img = None
    try:
        if os.path.exists("testlogo.png"):
            img = Image.open("testlogo.png").resize(LOGO_SIZE, Image.LANCZOS)
            logo_img = ImageTk.PhotoImage(img)
            logo = tk.Label(welcome_container, image=logo_img, borderwidth=0, bg=LEFT_BG)
            logo.image = logo_img # Keep a reference to prevent garbage collection
            logo.pack()
        else:
            logo = tk.Label(welcome_container, text="TrackU Logo", font=("Arial", 24, "bold"), bg=LEFT_BG, fg="darkgray")
            logo.pack()
            messagebox.showwarning("Image Warning", "testlogo.png not found. Using placeholder text.")
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load logo image:\n{e}. Using placeholder text.")
        logo = tk.Label(welcome_container, text="TrackU Logo", font=("Arial", 24, "bold"), bg=LEFT_BG, fg="darkgray")
        logo.pack()

    # Welcome text
    welcome1 = tk.Label(welcome_container, text="Welcome to", font=("Playfair Display", 48, "normal"), bg=LEFT_BG,
                        borderwidth=0)
    welcome1.pack(pady=(10, 0))

    welcome2 = tk.Label(welcome_container, text="TrackU", font=("Playfair Display", 42, "bold"), bg=LEFT_BG)
    welcome2.pack(pady=(0,0))

    # Tagline
    tagline = tk.Label(left_frame, text="Track your spending. Save\nsmart. Stress less.", font=FONT_SUB, bg=LEFT_BG, borderwidth=0)
    tagline.grid(row=1, column=0, pady=(0, 0))

    # Copyright text
    copyright = tk.Label(left_frame, text="© 2025 TrackU. All rights reserved.", font=("Georgia", 12), bg=LEFT_BG)
    copyright.grid(row=3, column=0, pady=(0, 20), sticky="s") # Anchor to bottom

    # --- Right Frame (Login Card & Grid) ---
    right_frame = tk.Frame(root, bg=RIGHT_BG)
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    # Main canvas for grid and card
    canvas = tk.Canvas(right_frame, bg=RIGHT_BG, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    # Rounded Card Canvas: This canvas will act as the container for the login form,
    # and it will be placed as a 'window' item on the main 'canvas'.
    # Its background will obscure the grid lines underneath it.
    rounded_card = tk.Canvas(canvas, width=CARD_WIDTH, height=CARD_HEIGHT, bg=RIGHT_BG, highlightthickness=0)
    # Store the ID returned by create_window to be able to tag_raise it
    card_window = canvas.create_window(0, 0, window=rounded_card, tags="login_card_window") # Initial dummy position

    def draw_grid():
        """Draws a grid on the main canvas."""
        canvas.delete("grid_line") # Clear previous grid lines
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        # Draw grid lines with a darker, thinner gray for better visibility
        # Added dash and capstyle for a "rounded" and less thick appearance
        for i in range(0, w, 30):
            canvas.create_line(i, 0, i, h, fill="#808080", width=1, tags="grid_line", dash=(1, 3), capstyle=tk.ROUND)
        for j in range(0, h, 30):
            canvas.create_line(0, j, w, j, fill="#808080", width=1, tags="grid_line", dash=(1, 3), capstyle=tk.ROUND)

        # Ensure the card is brought to the front AFTER grid is drawn
        # This makes sure the card's background covers the grid lines underneath it.
        canvas.tag_raise("login_card_window")

    def center_card(event=None):
        """Centers the login card on the canvas and redraws the grid."""
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w > 0 and h > 0:
            # Set the position of the window that contains rounded_card
            canvas.coords(card_window, w // 2, h // 2)
            # Ensure the card window is always on top after centering
            canvas.tag_raise("login_card_window")
        # Always redraw grid on configure to ensure it covers the available space
        draw_grid()

    # Bind configuration changes (resize) of the main canvas to center the card and redraw the grid
    canvas.bind("<Configure>", center_card)

    # Draw the initial rounded rectangle on the 'rounded_card' canvas
    draw_rounded_rect_on_canvas(rounded_card, 0, 0, CARD_WIDTH, CARD_HEIGHT, 30, CARD_BG, tags="card_background_shape")

    # Frame for login content (placed inside rounded_card canvas)
    card_frame = tk.Frame(rounded_card, width=CARD_WIDTH, height=CARD_HEIGHT, bg=CARD_BG)
    rounded_card.create_window(CARD_WIDTH // 2, CARD_HEIGHT // 2, window=card_frame)

    # Card Logo (inside the login card)
    card_logo_img = None
    try:
        if os.path.exists("testlogo.png"):
            img_card = Image.open("testlogo.png").resize(LOGO_SIZE, Image.LANCZOS)
            card_logo_img = ImageTk.PhotoImage(img_card)
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

    # Card Title
    card_title = tk.Label(card_frame, text="TrackU", font=("Playfair Display", 28, "bold"), bg=CARD_BG, borderwidth=0)
    card_title.pack(pady=(0, 10))

    # --- Custom Rounded Username Entry ---
    # Dimensions for the inner white entry area
    entry_inner_width, entry_inner_height, entry_inner_radius = 340, 48, 24
    # Dimensions for the outer black background of the entry
    entry_outer_width, entry_outer_height, entry_outer_radius = entry_inner_width + 38, entry_inner_height + 38, entry_inner_radius + 19

    # Create a frame to stack the black background canvas and the white foreground canvas
    entry_stack_frame = tk.Frame(card_frame, width=entry_outer_width, height=entry_outer_height, bg=CARD_BG)
    entry_stack_frame.pack(pady=(5, 10))
    entry_stack_frame.pack_propagate(False) # Prevent the frame from shrinking/expanding with contents

    # Canvas for the black rounded background of the entry field
    # IMPORTANT: Create and place this background canvas FIRST for correct stacking order
    bg_entry_canvas = tk.Canvas(entry_stack_frame, width=entry_outer_width, height=entry_outer_height, bg="black", highlightthickness=0)
    draw_rounded_rect_on_canvas(bg_entry_canvas, 0, 0, entry_outer_width, entry_outer_height, entry_outer_radius, "black")
    bg_entry_canvas.place(x=0, y=0) # Place it at 0,0 within the stack frame

    # Canvas for the white rounded foreground/entry area
    # IMPORTANT: Create and place this foreground canvas SECOND, so it naturally stacks on top
    fg_entry_canvas = tk.Canvas(entry_stack_frame, width=entry_inner_width, height=entry_inner_height, bg="white", highlightthickness=0)
    draw_rounded_rect_on_canvas(fg_entry_canvas, 0, 0, entry_inner_width, entry_inner_height, entry_inner_radius, "white")
    fg_entry_canvas.place(
        x=(entry_outer_width - entry_inner_width)//2, # Center horizontally within bg_entry_canvas
        y=(entry_outer_height - entry_inner_height)//2 # Center vertically within bg_entry_canvas
    )

    # Create the actual Entry widget inside the fg_entry_canvas as a window item
    username_var = tk.StringVar()
    username_entry = tk.Entry(fg_entry_canvas, textvariable=username_var, font=("Playfair Display", 18), bd=0, relief="flat", justify="center", fg="grey", bg="white")
    username_entry.insert(0, "Enter Username")
    # Place the entry within its foreground canvas
    fg_entry_canvas.create_window(entry_inner_width//2, entry_inner_height//2, window=username_entry,
                                  width=entry_inner_width-16, height=entry_inner_height-10)

    # Removed fg_entry_canvas.lift() - relying on place stacking order now.

    def on_entry_click(event):
        """Clears placeholder text on entry click."""
        if username_entry.get() == "Enter Username":
            username_entry.delete(0, tk.END)
            username_entry.config(fg='black')
    username_entry.bind("<FocusIn>", on_entry_click)

    # --- Login Button ---
    def login():
        """Handles the login process and launches the dashboard."""
        username = username_var.get()
        if username and username != "Enter Username":
            root.destroy()  # Close the login window
            try:
                # Adjust path to dashboard.py based on your folder structure
                # This path assumes dashboard.py is in a sibling folder named 'DASHBOARD'
                dashboard_path = os.path.join(os.path.dirname(__file__), "..", "DASHBOARD", "dashboard.py")
                subprocess.Popen(["python", dashboard_path])
            except Exception as e:
                messagebox.showerror("Launch Error", f"Failed to launch dashboard.py:\n{e}")
        else:
            messagebox.showerror("Login Error", "Please enter a valid username.")

    rounded_login_btn = create_rounded_button(
        card_frame, width=180, height=50, radius=25, bg_color=ACCENT, # Adjusted height and radius for button
        text="LOGIN", font=FONT_BTN, fg="black", command=login
    )
    rounded_login_btn.pack(pady=(10, 30))

    root.mainloop()

if __name__ == "__main__":
    create_login_app()