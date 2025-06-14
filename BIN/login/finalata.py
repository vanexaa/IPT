import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Colors and fonts
LEFT_BG = "#d6e9d5"
RIGHT_BG = "#fdf6e3"
CARD_BG = "#fbe3c0"
ACCENT = "#d6e9d5"
FONT_MAIN = ("Georgia", 36, "bold")
FONT_SUB = ("Georgia", 16)
FONT_BTN = ("Georgia", 20, "bold")


def create_app():
    # Main window
    root = tk.Tk()
    root.title("TrackU Login")
    root.geometry("1100x600")
    root.minsize(800, 500)

    # Make the grid expandable
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Left Frame
    left_frame = tk.Frame(root, bg=LEFT_BG)
    left_frame.grid(row=0, column=0, sticky="nsew")
    left_frame.grid_rowconfigure(0, weight=2)
    left_frame.grid_rowconfigure(1, weight=1)
    left_frame.grid_rowconfigure(2, weight=1)
    left_frame.grid_rowconfigure(3, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    # --- IMAGE TEMPLATE START ---
    # Replace 'your_logo.png' with your image file path
    try:
        img = Image.open("testlogo.png")  # Place your image in the same folder or give full path
        img = img.resize((100, 100), Image.LANCZOS)
        logo_img = ImageTk.PhotoImage(img)
        logo = tk.Label(left_frame, image=logo_img, bg=LEFT_BG)
        logo.image = logo_img  # Keep a reference
        logo.grid(row=0, column=0, pady=(10, 20), padx=30)
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load logo image:\n{e}")

    # Welcome Text
    welcome = tk.Label(left_frame, text="Welcome to\nTrackU", font=FONT_MAIN, bg=LEFT_BG)
    welcome.grid(row=1, column=0, pady=(10, 20), padx=30)

    # Tagline
    tagline = tk.Label(left_frame, text="Track your spending. Save\nsmart. Stress less.", font=FONT_SUB, bg=LEFT_BG)
    tagline.grid(row=2, column=0, pady=(10, 20), padx=30)

    # Copyright
    copyright = tk.Label(left_frame, text="© 2025 TrackU. All rights reserved.", font=("Georgia", 12), bg=LEFT_BG)
    copyright.grid(row=3, column=0, pady=(0, 20), padx=30, sticky="s")

    # Right Frame (background grid)
    right_frame = tk.Frame(root, bg=RIGHT_BG)
    right_frame.grid(row=0, column=1, sticky="nsew")
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    # Canvas for grid lines
    canvas = tk.Canvas(right_frame, bg=RIGHT_BG, highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    def draw_grid(event=None):
        canvas.delete("grid_line")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        for i in range(0, w, 30):
            canvas.create_line(i, 0, i, h, fill="#bdbdbd", width=1, tags="grid_line")
        for j in range(0, h, 30):
            canvas.create_line(0, j, w, j, fill="#bdbdbd", width=1, tags="grid_line")

    canvas.bind("<Configure>", draw_grid)

    # Rounded Card
    rounded_card = tk.Canvas(canvas, width=300, height=400, bg="#fefef5", highlightthickness=0)
    rounded_card.place(relx=0.5, rely=0.5, anchor="center")

    # Draw rounded rectangle manually
    def draw_rounded_rect(x, y, w, h, r, color):
        rounded_card.create_arc(x, y, x + 2*r, y + 2*r, start=90, extent=90, fill=color, outline=color)
        rounded_card.create_arc(x + w - 2*r, y, x + w, y + 2*r, start=0, extent=90, fill=color, outline=color)
        rounded_card.create_arc(x, y + h - 2*r, x + 2*r, y + h, start=180, extent=90, fill=color, outline=color)
        rounded_card.create_arc(x + w - 2*r, y + h - 2*r, x + w, y + h, start=270, extent=90, fill=color, outline=color)
        rounded_card.create_rectangle(x + r, y, x + w - r, y + h, fill=color, outline=color)
        rounded_card.create_rectangle(x, y + r, x + w, y + h - r, fill=color, outline=color)

    draw_rounded_rect(0, 0, 300, 400, 20, "#fce0b0")

    # Card Logo (template for image)
    try:
        card_img = Image.open("testlogo.png")  # Use the same or a different image
        card_img = card_img.resize((100, 100), Image.LANCZOS)
        card_logo_img = ImageTk.PhotoImage(card_img)
        card_logo = tk.Label(rounded_card, image=card_logo_img, bg="#fefef5")
        card_logo.image = card_logo_img
        card_logo.place(relx=0.5, rely=0.2, anchor="center")
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load logo image:\n{e}")

    # Card Title
    card_title = tk.Label(rounded_card, text="TrackU", font=("Georgia", 28, "bold"), bg="#fefef5")
    card_title.place(relx=0.5, rely=0.4, anchor="center")

    # Username Entry
    username_var = tk.StringVar()
    username_entry = tk.Entry(rounded_card, textvariable=username_var, font=("Georgia", 18), bd=2, relief="solid",
                              justify="center")
    username_entry.insert(0, "Enter Username")

    # Clear placeholder on focus
    def on_entry_click(event):
        if username_entry.get() == "Enter Username":
            username_entry.delete(0, tk.END)  # Clear the entry
            username_entry.config(fg='black')  # Change text color to black

    username_entry.bind("<FocusIn>", on_entry_click)
    username_entry.place(relx=0.5, rely=0.55, anchor="center", width=200, height=40)

    # Login Button
    def login():
        print("Username:", username_var.get())

    login_btn = tk.Button(rounded_card, text="LOGIN", font=FONT_BTN, bg=ACCENT, fg="black", width=12, bd=0, relief="flat",
                          command=login)
    login_btn.place(relx=0.5, rely=0.75, anchor="center")

    root.mainloop()


if __name__ == "__main__":
    create_app()
