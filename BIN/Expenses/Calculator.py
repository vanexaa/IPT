import tkinter as tk

root = tk.Tk()
root.title("Expense Entry")
root.geometry("900x520")
root.configure(bg="#faf6ef")
root.resizable(False, False)

# Main frame with rounded border simulation
main_frame = tk.Frame(root, bg="#faf6ef", highlightbackground="#222", highlightthickness=2, bd=0)
main_frame.place(x=20, y=20, width=860, height=480)

# Header
tk.Label(main_frame, text="❌", fg="red", bg="#faf6ef", font=("Arial", 18, "bold")).place(x=20, y=18)
tk.Label(main_frame, text="Cancel", fg="#222", bg="#faf6ef", font=("Georgia", 12, "bold")).place(x=55, y=23)
tk.Label(main_frame, text="Food", fg="#222", bg="#faf6ef", font=("Georgia", 26, "bold")).place(relx=0.5, y=18, anchor="n")
tk.Label(main_frame, text="Expenses", fg="#222", bg="#faf6ef", font=("Georgia", 16)).place(x=760, y=23)

# Amount Entry Display
display_frame = tk.Frame(main_frame, bg="#faf6ef", highlightbackground="#222", highlightthickness=2, bd=0)
display_frame.place(relx=0.5, y=90, anchor="n", width=220, height=55)
amount_var = tk.StringVar(value="₱ 0.00")
amount_label = tk.Label(display_frame, textvariable=amount_var, font=("Georgia", 20), bg="#faf6ef")
amount_label.pack(expand=True, fill="both")

# Checkmark button
check_btn = tk.Button(main_frame, text="✓", font=("Arial", 22, "bold"), bg="#ffe0b2", bd=0, relief="flat", width=2, height=1)
check_btn.place(relx=0.5, y=90, anchor="nw", x=130, width=55, height=55)

# Keypad buttons
btn_font = ("Georgia", 18)
btn_bg = "#ffe0b2"
btns = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['.', '0', '⌫']
]

def on_btn_click(val):
    current = amount_var.get().replace("₱ ", "").replace(",", "")
    if val == "⌫":
        current = current[:-1] if len(current) > 0 else ""
    elif val == ".":
        if "." not in current:
            current += "."
    else:
        if current == "0.00":
            current = ""
        current += val
    # Format display
    try:
        if current == "" or current == ".":
            display = "₱ 0.00"
        else:
            display = f"₱ {float(current):,.2f}"
    except:
        display = "₱ 0.00"
    amount_var.set(display)

# Center keypad in the main frame
keypad_start_x = 320
keypad_start_y = 180
btn_w = 90
btn_h = 60
btn_pad = 18

for i, row in enumerate(btns):
    for j, val in enumerate(row):
        b = tk.Button(main_frame, text=val, font=btn_font, bg=btn_bg, bd=0, relief="flat",
                      command=lambda v=val: on_btn_click(v))
        b.place(x=keypad_start_x + j*(btn_w+btn_pad), y=keypad_start_y + i*(btn_h+btn_pad), width=btn_w, height=btn_h)

root.mainloop()