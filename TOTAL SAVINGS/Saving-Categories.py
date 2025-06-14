import tkinter as tk
from tkinter import font

# ======== SavingsInputApp class =========
BG_COLOR = "#FCFAF2"
BTN_COLOR = "#FAD7A0"
BTN_ACTIVE = "#F9D7A0"
BORDER_COLOR = "#000"
FONT_FAMILY = "Georgia"

class SavingsInputApp(tk.Toplevel):
    def __init__(self, master=None, category="Food"):
        super().__init__(master)
        self.title("Savings Input")
        self.configure(bg=BG_COLOR)
        self.geometry("600x500")
        self.resizable(False, False)

        self.title_font = font.Font(family=FONT_FAMILY, size=22, weight="bold")
        self.label_font = font.Font(family=FONT_FAMILY, size=18)
        self.btn_font = font.Font(family=FONT_FAMILY, size=18)
        self.small_font = font.Font(family=FONT_FAMILY, size=13)

        self.category = category
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self, bg=BG_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=2)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=520, height=450)

        cancel_btn = tk.Button(main_frame, text="⛔", font=self.btn_font, bg="#E74C3C", fg="white",
                               bd=0, activebackground="#C0392B", command=self.destroy)
        cancel_btn.place(x=15, y=15, width=40, height=40)
        cancel_label = tk.Label(main_frame, text="Cancel", font=self.small_font, bg=BG_COLOR, fg=BORDER_COLOR)
        cancel_label.place(x=60, y=25)

        # Changed label from "Expenses" to "Savings"
        savings_label = tk.Label(main_frame, text="Savings", font=self.small_font, bg=BG_COLOR, fg=BORDER_COLOR)
        savings_label.place(x=420, y=25)

        title_label = tk.Label(main_frame, text=self.category, font=self.title_font, bg=BG_COLOR, fg=BORDER_COLOR)
        title_label.place(relx=0.5, y=60, anchor="center")

        entry_frame = tk.Frame(main_frame, bg=BTN_COLOR, bd=2, relief="groove")
        entry_frame.place(relx=0.5, y=110, anchor="center", width=220, height=50)

        currency_label = tk.Label(entry_frame, text="₱", font=self.label_font, bg=BTN_COLOR)
        currency_label.place(x=10, y=8)

        self.amount_var = tk.StringVar(value="0")
        amount_entry = tk.Entry(entry_frame, textvariable=self.amount_var, font=self.label_font,
                                bd=0, bg=BTN_COLOR, justify="right")
        amount_entry.place(x=40, y=8, width=110, height=30)

        def update_scroll(*args):
            amount_entry.xview_moveto(1)
        self.amount_var.trace_add("write", update_scroll)

        check_btn = tk.Button(main_frame, text="✔", font=self.btn_font, bg=BTN_COLOR, bd=0,
                              activebackground=BTN_ACTIVE, command=self.on_submit)
        check_btn.place(x=370, y=85, width=45, height=45)

        btns = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['.', '0', '⌫']
        ]

        btn_width = 60
        btn_height = 40
        padding_x = 10
        padding_y = 8

        total_width = 3 * btn_width + 2 * padding_x
        keypad_start_x = (520 - total_width) // 2
        keypad_start_y = 170

        for r, row in enumerate(btns):
            for c, char in enumerate(row):
                x_pos = keypad_start_x + c * (btn_width + padding_x)
                y_pos = keypad_start_y + r * (btn_height + padding_y)
                btn = tk.Button(main_frame, text=char, font=self.btn_font, bg=BTN_COLOR, bd=0,
                                activebackground=BTN_ACTIVE,
                                command=lambda ch=char: self.on_keypad(ch))
                btn.place(x=x_pos, y=y_pos, width=btn_width, height=btn_height)

    def on_keypad(self, char):
        if char == '⌫':
            current = self.amount_var.get()
            if len(current) > 1:
                self.amount_var.set(current[:-1])
            else:
                self.amount_var.set("0")
        elif char == '.':
            if '.' not in self.amount_var.get():
                self.amount_var.set(self.amount_var.get() + '.')
        else:
            current = self.amount_var.get()
            if current == "0":
                self.amount_var.set(char)
            else:
                self.amount_var.set(current + char)

    def on_submit(self):
        print("Submitted:", self.amount_var.get())

# ======== RoundedFrame class =========
class RoundedFrame(tk.Frame):
    def __init__(self, master=None, radius=25, bg="#FAD7A0", border_color="#000", border_width=2, **kwargs):
        super().__init__(master, bg=bg, **kwargs)
        self.radius = radius
        self.bg = bg
        self.border_color = border_color
        self.border_width = border_width
        self.canvas = tk.Canvas(self, bg=self.bg, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.bind("<Configure>", self._draw_rounded_rect)

        self.category_buttons = []
        self.header_height = 60

    def _draw_rounded_rect(self, event):
        self.canvas.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        r = self.radius
        header_height = self.header_height
        header_color = "#FAD7A0"

        self.canvas.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, fill=header_color, outline=header_color)
        self.canvas.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, fill=header_color, outline=header_color)
        self.canvas.create_rectangle((r, 0, w-r, header_height), fill=header_color, outline=header_color)
        self.canvas.create_rectangle((0, r, w, header_height), fill=header_color, outline=header_color)
        self.canvas.create_rectangle((0, header_height, w, h), fill=self.bg, outline=self.bg)

        self.canvas.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, style='arc', outline=self.border_color, width=self.border_width)
        self.canvas.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, style='arc', outline=self.border_color, width=self.border_width)
        self.canvas.create_arc((0, h-2*r, 2*r, h), start=180, extent=90, style='arc', outline=self.border_color, width=self.border_width)
        self.canvas.create_arc((w-2*r, h-2*r, w, h), start=270, extent=90, style='arc', outline=self.border_color, width=self.border_width)
        self.canvas.create_line(r, 0, w-r, 0, fill=self.border_color, width=self.border_width)
        self.canvas.create_line(r, h, w-r, h, fill=self.border_color, width=self.border_width)
        self.canvas.create_line(0, r, 0, h-r, fill=self.border_color, width=self.border_width)
        self.canvas.create_line(w, r, w, h-r, fill=self.border_color, width=self.border_width)

        self.canvas.create_text(w // 2, header_height // 2, text="CATEGORIES", font=("Times New Roman", 24, "bold"), fill="#000")

        close_btn = tk.Button(self.canvas, text="✕", font=("Arial", 28, "bold"), bg=header_color, bd=0,
                              activebackground=header_color, command=self.master.destroy)
        self.canvas.create_window(40, header_height // 2, window=close_btn, width=40, height=40)

        category_names = ["Food", "Future Purchase", "Emergency Fund", "Personal Goals", "General Savings"]

        emoji_map = {
            "Food": "🍽️",
            "Future Purchase": "🏷️",
            "Emergency Fund": "🚨",
            "Personal Goals": "🎯",
            "General Savings": "🏦"
        }

        btn_width = 200
        btn_height = 120
        spacing_x = 30
        spacing_y = 40
        btn_radius = 20

        for btn in self.category_buttons:
            btn.destroy()
        self.category_buttons.clear()

        def open_category_window(category_name):
            # Show SavingsInputApp for all categories
            if category_name in ["Food", "Future Purchase", "Emergency Fund", "Personal Goals", "General Savings"]:
                SavingsInputApp(self.master, category=category_name)
            else:
                new_win = tk.Toplevel(self)
                new_win.title(category_name)
                new_win.geometry("400x300")
                new_win.configure(bg="#FFFDF6")

                label = tk.Label(new_win, text=f"Welcome to {category_name} category!",
                                 font=("Arial", 16), bg="#FFFDF6")
                label.pack(pady=40)

        def draw_rounded_rect(canvas, x1, y1, x2, y2, r, color):
            canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, fill=color, outline=color)
            canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, fill=color, outline=color)
            canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, fill=color, outline=color)
            canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, fill=color, outline=color)
            canvas.create_rectangle(x1 + r, y1, x2 - r, y2, fill=color, outline=color)
            canvas.create_rectangle(x1, y1 + r, x2, y2 - r, fill=color, outline=color)

        def create_category_button(x_pos, y_pos, name):
            btn_canvas = tk.Canvas(self.canvas, width=btn_width, height=btn_height, bg="#FFFDF6", highlightthickness=0, cursor="hand2")

            def draw_button(bg_color):
                btn_canvas.delete("all")
                draw_rounded_rect(btn_canvas, 0, 0, btn_width, btn_height, btn_radius, bg_color)

                emoji_font = ("Segoe UI Emoji", 50)
                y_offset_map = {
                    "Food": 50,
                    "Future Purchase": 50,
                    "Emergency Fund": 45,
                    "Personal Goals": 45,
                    "General Savings": 45
                }

                btn_canvas.create_text(
                    btn_width // 2,
                    y_offset_map[name],
                    text=emoji_map[name],
                    font=emoji_font,
                    anchor="center"
                )

                btn_canvas.create_text(
                    btn_width // 2,
                    100,
                    text=name,
                    font=("Arial", 14),
                    anchor="center"
                )

            draw_button("#FAD7A0")
            btn_canvas.bind("<Button-1>", lambda e: open_category_window(name))
            btn_canvas.bind("<Enter>", lambda e: draw_button("#D6EAF8"))
            btn_canvas.bind("<Leave>", lambda e: draw_button("#FAD7A0"))

            self.canvas.create_window(x_pos, y_pos, window=btn_canvas)
            self.category_buttons.append(btn_canvas)

        row1_count = 3
        total_width_row1 = row1_count * btn_width + (row1_count - 1) * spacing_x
        start_x_row1 = (w - total_width_row1) // 2 + btn_width // 2
        y_pos_row1 = header_height + 70

        row2_count = 2
        total_width_row2 = row2_count * btn_width + (row2_count - 1) * spacing_x
        start_x_row2 = (w - total_width_row2) // 2 + btn_width // 2
        y_pos_row2 = y_pos_row1 + btn_height + spacing_y

        for i in range(row1_count):
            name = category_names[i]
            x_pos = start_x_row1 + i * (btn_width + spacing_x)
            create_category_button(x_pos, y_pos_row1, name)

        for i in range(row2_count):
            name = category_names[row1_count + i]
            x_pos = start_x_row2 + i * (btn_width + spacing_x)
            create_category_button(x_pos, y_pos_row2, name)

# ======== Main window =========
root = tk.Tk()
root.title("Categories")
root.configure(bg="#FFFDF6")
root.geometry("800x500")
root.resizable(False, False)

main_frame = RoundedFrame(root, radius=30, bg="#FFFDF6", border_color="#000", border_width=2)
main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=750, height=420)

root.mainloop()