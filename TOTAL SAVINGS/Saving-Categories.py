import tkinter as tk
from tkinter import font
import tkinter.messagebox
import sys
import os

# --- Path setup for database_manager.py ---
current_script_dir = os.path.dirname(__file__)
database_folder_path = os.path.abspath(os.path.join(current_script_dir, "..", "TOTAL EXPENSES"))
if database_folder_path not in sys.path:
    sys.path.append(database_folder_path)
# ------------------------------------------

import database_manager

BG_COLOR = "#FCFAF2"
BTN_COLOR = "#FAD7A0"
BTN_ACTIVE = "#F9D7A0"
BORDER_COLOR = "#000"
FONT_FAMILY = "Georgia"
SAVINGS_CATEGORIES = ["Emergency Fund", "Future Purchase", "Personal Goals", "General Savings"]

def center_toplevel_window(window):
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f"+{x}+{y}")

class SavingsInputApp(tk.Toplevel):
    def __init__(self, master=None, category="General Savings"):
        super().__init__(master)
        self.title("Savings Input")
        self.configure(bg=BG_COLOR)
        self.geometry("600x500")
        self.resizable(False, False)
        self.overrideredirect(True)
        self.title_font = font.Font(family=FONT_FAMILY, size=22, weight="bold")
        self.label_font = font.Font(family=FONT_FAMILY, size=18)
        self.btn_font = font.Font(family=FONT_FAMILY, size=18)
        self.small_font = font.Font(family=FONT_FAMILY, size=13)
        self.category = category
        self.create_widgets()
        center_toplevel_window(self)

    def create_widgets(self):
        main_frame = tk.Frame(self, bg=BG_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=2)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=520, height=450)
        cancel_btn = tk.Button(main_frame, text="⛔", font=self.btn_font, bg="#E74C3C", fg="white",
                               bd=0, activebackground="#C0392B", command=self.destroy)
        cancel_btn.place(x=15, y=15, width=40, height=40)
        cancel_label = tk.Label(main_frame, text="Cancel", font=self.small_font, bg=BG_COLOR, fg=BORDER_COLOR)
        cancel_label.place(x=60, y=25)
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
        current = self.amount_var.get()
        if char == '⌫':
            if len(current) > 1:
                self.amount_var.set(current[:-1])
            else:
                self.amount_var.set("0")
        elif char == '.':
            if '.' not in current:
                self.amount_var.set(current + '.')
        else:
            if current == "0" and char != "0":
                self.amount_var.set(char)
            elif current == "0" and char == "0":
                pass
            else:
                self.amount_var.set(current + char)

    def on_submit(self):
        try:
            amount = float(self.amount_var.get())
            if amount <= 0:
                tk.messagebox.showerror("Invalid Input", "Amount must be greater than zero.")
                return
            success = database_manager.add_savings_record(self.category, amount)
            if success:
                print(f"Submitted savings: ₱{amount:.2f} for category '{self.category}'")
                tk.messagebox.showinfo("Success", f"Savings of ₱{amount:,.2f} added to {self.category}!")
                self.destroy()
            else:
                tk.messagebox.showerror("Database Error", "Failed to save savings record.")
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter a valid numeric amount.")

class RoundedFrame(tk.Frame):
    def __init__(self, master=None, radius=25, bg="#FFFDF6", border_color="#000", border_width=2, **kwargs):
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
        self._x = 0
        self._y = 0
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        if event.y < self.header_height:
            self._x = event.x
            self._y = event.y

    def do_move(self, event):
        if self._x is not None and self._y is not None and event.y < self.header_height:
            deltax = event.x - self._x
            deltay = event.y - self._y
            x = self.master.winfo_x() + deltax
            y = self.master.winfo_y() + deltay
            self.master.geometry(f"+{x}+{y}")

    def _draw_rounded_rect(self, event):
        self.canvas.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        r = self.radius
        header_height = self.header_height
        header_color = BTN_COLOR

        # Draw rounded corners for the main window
        self.canvas.create_arc((0, 0, 2 * r, 2 * r), start=90, extent=90, fill=self.bg, outline=self.bg)
        self.canvas.create_arc((w - 2 * r, 0, w, 2 * r), start=0, extent=90, fill=self.bg, outline=self.bg)
        self.canvas.create_arc((0, h - 2 * r, 2 * r, h), start=180, extent=90, fill=self.bg, outline=self.bg)
        self.canvas.create_arc((w - 2 * r, h - 2 * r, w, h), start=270, extent=90, fill=self.bg, outline=self.bg)
        self.canvas.create_rectangle((r, 0, w - r, h), fill=self.bg, outline=self.bg)
        self.canvas.create_rectangle((0, r, w, h - r), fill=self.bg, outline=self.bg)

        # Draw the header as a straight rectangle (not rounded)
        self.canvas.create_rectangle((0, 0, w, header_height), fill=header_color, outline=header_color)

        # Draw a horizontal line to separate content and header
        self.canvas.create_line(0, header_height, w, header_height, fill=header_color, width=self.border_width)

        # Header text and close button
        self.canvas.create_text(w // 2, header_height // 2, text="CATEGORIES", font=("Times New Roman", 24, "bold"),
                                fill="#000")
        close_btn = tk.Button(self.canvas, text="✕", font=("Arial", 28, "bold"), bg=header_color, bd=0,
                              activebackground=header_color, command=self.master.destroy)
        self.canvas.create_window(40, header_height // 2, window=close_btn, width=40, height=40)
        self._draw_category_buttons()

    def _draw_category_buttons(self):
        for btn_item in self.category_buttons:
            window_widget = self.canvas.itemcget(btn_item, "window")
            if window_widget:
                widget_instance = self.nametowidget(window_widget)
                widget_instance.destroy()
            self.canvas.delete(btn_item)
        self.category_buttons.clear()
        categories_to_display = SAVINGS_CATEGORIES
        emoji_map = {
            "Emergency Fund": "🚨",
            "Future Purchase": "🏷️",
            "Personal Goals": "🎯",
            "General Savings": "🏦"
        }
        btn_width = 200
        btn_height = 120
        spacing_x = 30
        spacing_y = 40
        btn_radius = 20
        start_y_for_categories = self.header_height + 90
        w = self.winfo_width()
        num_categories = len(categories_to_display)
        current_y_pos = start_y_for_categories

        def open_category_input_window(category_name):
            SavingsInputApp(self.master, category=category_name)

        def draw_rounded_rect_on_canvas(canvas, x1, y1, x2, y2, r, color):
            canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, fill=color, outline=color)
            canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, fill=color, outline=color)
            canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, fill=color, outline=color)
            canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, fill=color, outline=color)
            canvas.create_rectangle(x1 + r, y1, x2 - r, y2, fill=color, outline=color)
            canvas.create_rectangle(x1, y1 + r, x2, y2 - r, fill=color, outline=color)

        def create_category_button_internal(x_pos, y_pos, name):
            btn_canvas = tk.Canvas(self.canvas, width=btn_width, height=btn_height, bg="#FFFDF6", highlightthickness=0,
                                   cursor="hand2")
            def draw_button(bg_color):
                btn_canvas.delete("all")
                draw_rounded_rect_on_canvas(btn_canvas, 0, 0, btn_width, btn_height, btn_radius, bg_color)
                emoji_font = ("Segoe UI Emoji", 50)
                emoji_y_pos = btn_height * 0.4
                text_y_pos = btn_height * 0.8
                btn_canvas.create_text(
                    btn_width // 2,
                    emoji_y_pos,
                    text=emoji_map.get(name, "❓"),
                    font=emoji_font,
                    anchor="center"
                )
                btn_canvas.create_text(
                    btn_width // 2,
                    text_y_pos,
                    text=name,
                    font=("Arial", 14),
                    anchor="center"
                )
            draw_button(BTN_COLOR)
            btn_canvas.bind("<Button-1>", lambda e: open_category_input_window(name))
            btn_canvas.bind("<Enter>", lambda e: draw_button(BTN_ACTIVE))
            btn_canvas.bind("<Leave>", lambda e: draw_button(BTN_COLOR))
            btn_item = self.canvas.create_window(x_pos, y_pos, window=btn_canvas)
            self.category_buttons.append(btn_item)

        if num_categories == 4:
            row_capacity_2x2 = 2
            total_width_2x2_row = row_capacity_2x2 * btn_width + (row_capacity_2x2 - 1) * spacing_x
            start_x_offset_2x2 = (w - total_width_2x2_row) // 2 + btn_width // 2
            for r in range(2):
                for c in range(row_capacity_2x2):
                    idx = r * row_capacity_2x2 + c
                    if idx < num_categories:
                        name = categories_to_display[idx]
                        x_pos = start_x_offset_2x2 + c * (btn_width + spacing_x)
                        y_pos = current_y_pos + r * (btn_height + spacing_y)
                        create_category_button_internal(x_pos, y_pos, name)
        else:
            row_capacity_general = 3
            for i in range(0, num_categories, row_capacity_general):
                row_categories = categories_to_display[i: i + row_capacity_general]
                current_row_width = len(row_categories) * btn_width + (len(row_categories) - 1) * spacing_x
                current_row_start_x = (w - current_row_width) // 2 + btn_width // 2
                for j, name in enumerate(row_categories):
                    x_pos = current_row_start_x + j * (btn_width + spacing_x)
                    create_category_button_internal(x_pos, current_y_pos, name)
                current_y_pos += btn_height + spacing_y

def create_categories_window():
    root = tk.Tk()
    root.title("Categories")
    root.configure(bg="#FFFDF6")
    root.geometry("800x500")
    root.resizable(False, False)
    root.overrideredirect(True)
    center_toplevel_window(root)
    main_frame = RoundedFrame(root, radius=30, bg="#FFFDF6", border_color="#000", border_width=2)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=750, height=420)
    root.mainloop()

if __name__ == "__main__":
    create_categories_window()