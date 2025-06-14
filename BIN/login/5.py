import tkinter as tk
from tkinter import messagebox

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

# Dynamic layout handler
def on_resize(event):
    w = root.winfo_width()
    h = root.winfo_height()

    left_frame.config(width=int(w * 0.35), height=h)
    canvas.config(width=int(w * 0.65), height=h)
    card.place(x=int((w * 0.65 - 300) / 2), y=int((h - 400) / 2))

    # Redraw grid
    canvas.delete("grid_line")
    for x in range(0, int(w * 0.65), 25):
        canvas.create_line(x, 0, x, h, fill="#ccc", tags="grid_line")
    for y in range(0, h, 25):
        canvas.create_line(0, y, int(w * 0.65), y, fill="#ccc", tags="grid_line")

root.bind("<Configure>", on_resize)

# Left Panel
left_frame = tk.Frame(root, bg="#d9e8d3")
left_frame.place(relx=0, rely=0, relheight=1, relwidth=0.35)

left_logo = tk.Canvas(left_frame, width=100, height=100, bg="#d9e8d3", highlightthickness=0)
left_logo.place(relx=0.35, y=60)
draw_logo(left_logo, 10, 80)

tk.Label(left_frame, text="Welcome to", bg="#d9e8d3", font=("Georgia", 24)).place(relx=0.2, y=150)
tk.Label(left_frame, text="TrackU", bg="#d9e8d3", font=("Georgia", 24, "bold")).place(relx=0.3, y=190)

tk.Label(left_frame, text="Track your spending. Save\nsmart. Stress less.",
         bg="#d9e8d3", font=("Georgia", 12), justify="center").place(relx=0.1, y=270)

tk.Label(left_frame, text="© 2025 TrackU. All rights reserved.",
         bg="#d9e8d3", font=("Georgia", 10)).place(relx=0.05, rely=0.95)

# Right grid background
canvas = tk.Canvas(root, bg="#fefef5", highlightthickness=0)
canvas.place(relx=0.35, rely=0, relwidth=0.65, relheight=1)

# Login Card
card = tk.Frame(canvas, bg="#fce0b0", width=300, height=400, bd=0, highlightthickness=0)

# Card Logo
card_logo = tk.Canvas(card, width=100, height=100, bg="#fce0b0", highlightthickness=0)
card_logo.place(x=100, y=30)
draw_logo(card_logo, 10, 80)

tk.Label(card, text="TrackU", bg="#fce0b0", font=("Georgia", 18)).place(x=110, y=120)

username_entry = tk.Entry(card, font=("Georgia", 11), width=25, bd=2, relief="solid", justify="center")
username_entry.place(x=55, y=170)

def login():
    username = username_entry.get()
    if username:
        messagebox.showinfo("Login", f"Welcome, {username}!")
    else:
        messagebox.showwarning("Login", "Please enter your username.")

login_btn = tk.Button(card, text="LOGIN", bg="#d1efe4", font=("Georgia", 12),
                      command=login, width=15, bd=0, relief="flat")
login_btn.place(x=80, y=220)

# Show card initially
card.place(x=650 - 300 // 2, y=90)

root.mainloop()
