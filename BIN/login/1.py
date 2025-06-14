import tkinter as tk
from tkinter import messagebox

# Add a method to draw rounded rectangles
def _create_round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return self.create_polygon(points, **kwargs, smooth=True)
tk.Canvas.create_round_rectangle = _create_round_rectangle

# Main Window
root = tk.Tk()
root.title("TrackU Login")
root.geometry("1000x580")
root.configure(bg="#fefef5")

# Function to draw the logo
def draw_logo(canvas, x, y):
    canvas.delete("all")
    canvas.create_rectangle(x, y, x+15, y-40, fill="#778195", width=0)
    canvas.create_rectangle(x+25, y, x+40, y-60, fill="#778195", width=0)
    canvas.create_rectangle(x+50, y, x+65, y-30, fill="#778195", width=0)

# Handle resizing
def on_resize(event):
    w = root.winfo_width()
    h = root.winfo_height()

    left_frame.config(width=int(w * 0.35), height=h)
    canvas.config(width=int(w * 0.65), height=h)

    canvas.delete("grid_line")
    for x in range(0, int(w * 0.65), 25):
        canvas.create_line(x, 0, x, h, fill="#ccc", tags="grid_line")
    for y in range(0, h, 25):
        canvas.create_line(0, y, int(w * 0.65), y, fill="#ccc", tags="grid_line")

    # Reposition centered text
    center_x = int(w * 0.35 / 2)
    welcome_label.place(x=center_x, y=150, anchor="center")
    tracku_label.place(x=center_x, y=190, anchor="center")

    # Move login card
    card_x = (w * 0.65 - 300) / 2
    card_y = (h - 400) / 2
    canvas.coords(card_bg, card_x, card_y, card_x + 300, card_y + 400)
    canvas.coords(card_window, card_x + 150, card_y + 200)

root.bind("<Configure>", on_resize)

# Left Panel
left_frame = tk.Frame(root, bg="#d9e8d3")
left_frame.place(relx=0, rely=0, relheight=1, relwidth=0.35)

left_logo = tk.Canvas(left_frame, width=100, height=100, bg="#d9e8d3", highlightthickness=0)
left_logo.place(relx=0.35, y=60)
draw_logo(left_logo, 10, 80)

welcome_label = tk.Label(left_frame, text="Welcome to", bg="#d9e8d3", font=("Georgia", 24))
welcome_label.place(x=175, y=150, anchor="center")

tracku_label = tk.Label(left_frame, text="TrackU", bg="#d9e8d3", font=("Georgia", 24, "bold"))
tracku_label.place(x=175, y=190, anchor="center")

tk.Label(left_frame, text="Track your spending. Save\nsmart. Stress less.",
         bg="#d9e8d3", font=("Georgia", 12), justify="center").place(relx=0.1, y=270)

tk.Label(left_frame, text="© 2025 TrackU. All rights reserved.",
         bg="#d9e8d3", font=("Georgia", 10)).place(relx=0.05, rely=0.95)

# Right Panel with Grid Background
canvas = tk.Canvas(root, bg="#fefef5", highlightthickness=0)
canvas.place(relx=0.35, rely=0, relwidth=0.65, relheight=1)

# Rounded login card on canvas
card_bg = canvas.create_round_rectangle(150, 100, 450, 500, radius=30, fill="#fce0b0", outline="")

# Card content
login_frame = tk.Frame(canvas, bg="#fce0b0")
card_window = canvas.create_window(300, 300, window=login_frame)

card_logo = tk.Canvas(login_frame, width=100, height=100, bg="#fce0b0", highlightthickness=0)
card_logo.pack(pady=(10, 0))
draw_logo(card_logo, 10, 80)

tk.Label(login_frame, text="TrackU", bg="#fce0b0", font=("Georgia", 18)).pack(pady=(5, 10))

username_entry = tk.Entry(login_frame, font=("Georgia", 11), width=25, bd=2, relief="solid", justify="center")
username_entry.pack(pady=(10, 10))

def login():
    username = username_entry.get()
    if username:
        messagebox.showinfo("Login", f"Welcome, {username}!")
    else:
        messagebox.showwarning("Login", "Please enter your username.")

login_btn = tk.Button(login_frame, text="LOGIN", bg="#d1efe4", font=("Georgia", 12),
                      command=login, width=15, bd=0, relief="flat")
login_btn.pack(pady=(10, 10))

# Initial layout adjustment
root.after(100, lambda: on_resize(None))

root.mainloop()
