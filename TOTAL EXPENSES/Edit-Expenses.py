import tkinter as tk
from tkinter import font, ttk
import tkinter.messagebox
import sys
import os
from datetime import datetime

# --- Path setup for database_manager.py ---
current_script_dir = os.path.dirname(__file__)

if current_script_dir not in sys.path:
    sys.sys.path.append(current_script_dir)  # Corrected to sys.path.append

import database_manager

BG_COLOR = "#FCFAF2"
BTN_COLOR = "#FAD7A0"
BTN_ACTIVE = "#F9D7A0"
BORDER_COLOR = "#000"
FONT_FAMILY = "Georgia"

# Categories for Expenses
EXPENSE_CATEGORIES = [
    "Food", "Transportation", "Utilities", "Rent", "Shopping",
    "Entertainment", "Health", "Education", "Salary", "Others"
]


def center_toplevel_window(window):
    """Centers a Tkinter Toplevel window on the screen."""
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f"+{x}+{y}")


class ExpenseInputApp(tk.Toplevel):
    """
    A Toplevel window for inputting expense amounts for a specific category.
    Supports both adding new expenses and updating existing ones.
    """

    def __init__(self, master=None, category="Others", record_id=None, initial_amount=0.0):
        super().__init__(master)
        self.title("Expense Input")
        self.configure(bg=BG_COLOR)
        self.geometry("600x500")
        self.resizable(False, False)
        self.overrideredirect(True)
        self.title_font = font.Font(family=FONT_FAMILY, size=22, weight="bold")
        self.label_font = font.Font(family=FONT_FAMILY, size=18)
        self.btn_font = font.Font(family=FONT_FAMILY, size=18)
        self.small_font = font.Font(family=FONT_FAMILY, size=13)
        self.category = category
        self.record_id = record_id
        self.initial_amount = initial_amount

        self.create_widgets()
        center_toplevel_window(self)

    def create_widgets(self):
        """Creates and places all widgets for the expense input window."""
        main_frame = tk.Frame(self, bg=BG_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=2)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=520, height=450)

        # Cancel button (X icon)
        cancel_btn = tk.Button(main_frame, text="⛔", font=self.btn_font, bg="#E74C3C", fg="white",
                               bd=0, activebackground="#C0392B", command=self.destroy)
        cancel_btn.place(x=15, y=15, width=40, height=40)
        cancel_label = tk.Label(main_frame, text="Cancel", font=self.small_font, bg=BG_COLOR, fg=BORDER_COLOR)
        cancel_label.place(x=60, y=25)

        # Expenses label
        expenses_label = tk.Label(main_frame, text="Expenses", font=self.small_font, bg=BG_COLOR, fg=BORDER_COLOR)
        expenses_label.place(x=400, y=25)

        # Category title label
        title_label = tk.Label(main_frame, text=self.category, font=self.title_font, bg=BG_COLOR, fg=BORDER_COLOR)
        title_label.place(relx=0.5, y=60, anchor="center")

        # Keypad button properties for calculation
        btn_width = 60
        btn_height = 40
        padding_x = 10
        padding_y = 8

        # Calculate the total width of the keypad
        total_keypad_width = 3 * btn_width + 2 * padding_x

        # Calculate absolute x position to center the keypad within main_frame
        keypad_start_x_abs = (520 - total_keypad_width) // 2

        # Adjusted keypad_start_y (original position before notes field was added)
        keypad_start_y = 160

        # --- Input Field and Check Button Positioning ---
        entry_frame_width = (2 * btn_width) + padding_x
        entry_height = 50

        check_btn_width = btn_width
        check_btn_height = 45

        # Determine x-position for the entry frame
        entry_frame_x = keypad_start_x_abs

        # Determine x-position for the check button
        check_btn_x = keypad_start_x_abs + 2 * (btn_width + padding_x)

        # Calculate y-positions for the input row
        entry_frame_y = keypad_start_y - entry_height - padding_y

        # Center the check button vertically with the entry frame
        check_btn_y = entry_frame_y + (entry_height - check_btn_height) // 2

        entry_frame = tk.Frame(main_frame, bg=BTN_COLOR, bd=2, relief="groove")
        entry_frame.place(x=entry_frame_x, y=entry_frame_y, width=entry_frame_width, height=entry_height)

        currency_label = tk.Label(entry_frame, text="₱", font=self.label_font, bg=BTN_COLOR)
        currency_label.place(x=10, y=8)

        self.amount_var = tk.StringVar(value=str(self.initial_amount) if self.record_id is not None else "0")

        amount_entry = tk.Entry(entry_frame, textvariable=self.amount_var, font=self.label_font,
                                bd=0, bg=BTN_COLOR, justify="right")
        amount_entry.place(x=40, y=8, width=entry_frame_width - 50, height=30)

        def update_scroll(*args):
            amount_entry.xview_moveto(1)

        self.amount_var.trace_add("write", update_scroll)

        check_btn = tk.Button(main_frame, text="✔", font=self.btn_font, bg=BTN_COLOR, bd=0,
                              activebackground=BTN_ACTIVE, command=self.on_submit)
        check_btn.place(x=check_btn_x, y=check_btn_y, width=check_btn_width, height=check_btn_height)

        # --- Keypad Buttons ---
        btns = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['.', '0', '⌫']
        ]
        for r, row in enumerate(btns):
            for c, char in enumerate(row):
                x_pos = keypad_start_x_abs + c * (btn_width + padding_x)
                y_pos = keypad_start_y + r * (btn_height + padding_y)
                btn = tk.Button(main_frame, text=char, font=self.btn_font, bg=BTN_COLOR, bd=0,
                                activebackground=BTN_ACTIVE,
                                command=lambda ch=char: self.on_keypad(ch))
                btn.place(x=x_pos, y=y_pos, width=btn_width, height=btn_height)

    def on_keypad(self, char):
        """Handles keypad button presses."""
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
        """Handles the submission of the expense amount."""
        try:
            amount = float(self.amount_var.get())

            if amount <= 0:
                tk.messagebox.showerror("Invalid Input", "Amount must be greater than zero.")
                return

            success = False
            if self.record_id is not None:
                # If record_id is present, attempt to update the existing record
                success = database_manager.update_expense_record(self.record_id, self.category, amount)
                if success:
                    tk.messagebox.showinfo("Success",
                                           f"Expense record (ID: {self.record_id}) updated to ₱{amount:,.2f} for {self.category}!")
                else:
                    tk.messagebox.showerror("Database Error", "Failed to update expense record.")
            else:
                # If no record_id, add a new expense record
                success = database_manager.add_expense_record(self.category, amount)
                if success:
                    tk.messagebox.showinfo("Success", f"Expense of ₱{amount:,.2f} added to {self.category}!")
                else:
                    tk.messagebox.showerror("Database Error", "Failed to save new expense record.")

            if success:
                self.destroy()
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter a valid numeric amount.")


class SelectExpenseToEditWindow(tk.Toplevel):
    """
    A Toplevel window for selecting an existing expense record to edit or delete.
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Select Expense to Edit")
        self.configure(bg=BG_COLOR)
        self.geometry("800x600")
        self.resizable(False, False)
        self.overrideredirect(True)
        center_toplevel_window(self)

        self.records_frame = tk.Frame(self, bg=BG_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=2)
        self.records_frame.place(relx=0.5, rely=0.5, anchor="center", width=750, height=550)

        self.create_widgets()
        self.load_expense_records()

    def create_widgets(self):
        """Creates the widgets for the record selection window."""
        # Header/Navbar
        header_height = 60
        header_color = BTN_COLOR
        header_label = tk.Label(self.records_frame, text="SELECT EXPENSE TO EDIT/DELETE",
                                font=("Times New Roman", 18, "bold"),
                                bg=header_color, fg="#000")
        header_label.place(relx=0.5, y=header_height // 2, anchor="center", relwidth=1)

        # Close button
        close_btn = tk.Button(self.records_frame, text="✕", font=("Arial", 20, "bold"), bg=header_color, bd=0,
                              activebackground=header_color, command=self.destroy)
        close_btn.place(x=10, y=header_height // 2, anchor="w", width=40, height=40)

        # Treeview for displaying records
        self.tree = ttk.Treeview(self.records_frame, columns=("ID", "Category", "Amount", "Date"),
                                 show="headings")
        self.tree.place(x=20, y=header_height + 20, width=710, height=350)

        # Setup headings
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Category", text="Category", anchor="w")
        self.tree.heading("Amount", text="Amount", anchor="e")
        self.tree.heading("Date", text="Date", anchor="center")

        # Setup columns - adjusted widths
        self.tree.column("ID", width=70, stretch=tk.NO, anchor="center")
        self.tree.column("Category", width=200, stretch=tk.NO)
        self.tree.column("Amount", width=150, stretch=tk.NO, anchor="e")
        self.tree.column("Date", width=290, stretch=tk.YES, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.records_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=730, y=header_height + 20, height=350)

        # Edit and Delete Buttons
        edit_btn = RoundedCanvasButton(
            self.records_frame,
            text="Edit Selected",
            command=self.edit_selected_record,
            radius=20,
            bg_color=BTN_COLOR,
            text_color=BORDER_COLOR,
            font=(FONT_FAMILY, 14, "bold")
        )
        edit_btn.place(relx=0.25, rely=0.9, anchor="center", width=180, height=50)

        delete_btn = RoundedCanvasButton(
            self.records_frame,
            text="Delete Selected",
            command=self.delete_selected_record,
            radius=20,
            bg_color="#E74C3C",
            text_color="white",
            font=(FONT_FAMILY, 14, "bold")
        )
        delete_btn.place(relx=0.75, rely=0.9, anchor="center", width=180, height=50)

    def load_expense_records(self):
        """Loads expense records from the database and populates the Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = database_manager.get_all_expenses()
        for record in records:
            # CORRECTED: Unpack 4 values, as database_manager.get_all_expenses() now returns 4 columns.
            record_id, category, amount, date_str = record

            # Format date for display
            formatted_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
            self.tree.insert("", "end", values=(record_id, category, f"₱{amount:,.2f}", formatted_date))

    def edit_selected_record(self):
        """Opens the ExpenseInputApp to edit the selected record."""
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("No Selection", "Please select an expense record to edit.")
            return

        values = self.tree.item(selected_item[0], 'values')
        record_id = int(values[0])
        category = values[1]
        amount_str = values[2].replace("₱", "").replace(",", "")
        initial_amount = float(amount_str)

        self.destroy()
        ExpenseInputApp(self.master, category=category, record_id=record_id, initial_amount=initial_amount)

    def delete_selected_record(self):
        """Deletes the selected expense record from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("No Selection", "Please select an expense record to delete.")
            return

        values = self.tree.item(selected_item[0], 'values')
        record_id = int(values[0])
        category = values[1]
        amount = values[2]

        confirm = tk.messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the expense record for '{category}' (Amount: {amount})?"
        )
        if confirm:
            if database_manager.delete_expense_record(record_id):
                tk.messagebox.showinfo("Success", "Expense record deleted successfully.")
                self.load_expense_records()
            else:
                tk.messagebox.showerror("Error", "Failed to delete expense record.")


class RoundedFrame(tk.Frame):
    """
    A custom Tkinter Frame with rounded corners and a draggable header.
    This class is primarily used for the category selection grid (which is now removed from 'Add New' flow).
    It is kept for backward compatibility with `ExpenseInputApp` potentially using it, if it were to be re-introduced.
    """

    def __init__(self, master=None, radius=25, bg="#FFFDF6", border_color="#000", border_width=2, **kwargs):
        super().__init__(master, bg=bg, **kwargs)
        self.master = master
        self.radius = radius
        self.bg = bg
        self.border_color = border_color
        self.border_width = border_width
        self.config(bd=0, highlightthickness=0)
        self.canvas = tk.Canvas(self, bg=self.master['bg'], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.bind("<Configure>", self._draw_rounded_rect)
        self.category_buttons = []
        self.header_height = 60
        self._x = 0
        self._y = 0
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        """Records the starting position for dragging."""
        if 0 <= event.y < self.header_height:
            self._x = event.x
            self._y = event.y
        else:
            self._x = None
            self._y = None

    def do_move(self, event):
        """Moves the window based on mouse drag."""
        if self._x is not None and self._y is not None:
            deltax = event.x - self._x
            deltay = event.y - self._y
            x = self.master.winfo_x() + deltax
            y = self.master.winfo_y() + deltay
            self.master.geometry(f"+{x}+{y}")

    def _draw_rounded_rect(self, event):
        """Draws the rounded rectangle shape on the canvas."""
        self.canvas.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        r = self.radius
        header_height = self.header_height
        header_color = BTN_COLOR
        fill_color = self.bg

        # Draw main rounded rectangle (overall window shape)
        self.canvas.create_arc((0, 0, 2 * r, 2 * r), start=90, extent=90, fill=fill_color, outline="")
        self.canvas.create_arc((w - 2 * r, 0, w, 2 * r), start=0, extent=90, fill=fill_color, outline="")
        self.canvas.create_arc((0, h - 2 * r, 2 * r, h), start=180, extent=90, fill=fill_color, outline="")
        self.canvas.create_arc((w - 2 * r, h - 2 * r, w, h), start=270, extent=90, fill=fill_color, outline="")
        self.canvas.create_rectangle((r, 0, w - r, h), fill=fill_color, outline="")
        self.canvas.create_rectangle(0, r, w, h - r, fill=fill_color, outline="")

        # Draw the header section (the 'navbar')
        self.canvas.create_rectangle(0, 0, w, header_height - r, fill=header_color, outline="")
        self.canvas.create_rectangle(r, 0, w - r, header_height, fill=header_color, outline="")

        # Bottom rounded corners of the header
        self.canvas.create_arc(0, header_height - 2 * r, 2 * r, header_height, start=180, extent=90, fill=header_color,
                               outline="")
        self.canvas.create_arc(w - 2 * r, header_height - 2 * r, w, header_height, start=270, extent=90,
                               fill=header_color, outline="")

        # Header text and close button
        self.canvas.create_text(w // 2, header_height // 2, text="CATEGORIES", font=("Times New Roman", 24, "bold"),
                                fill="#000")
        close_btn = tk.Button(self.canvas, text="✕", font=("Arial", 28, "bold"), bg=header_color, bd=0,
                              activebackground=header_color, command=self.master.destroy)
        self.canvas.create_window(40, header_height // 2, window=close_btn, width=40, height=40)


class RoundedCanvasButton(tk.Canvas):
    """
    A custom Tkinter Canvas widget that acts like a button with rounded corners.
    It draws its own background and text, providing full control over appearance.
    """

    def __init__(self, master, text, command=None, radius=20, bg_color=BTN_COLOR, text_color=BORDER_COLOR,
                 font=(FONT_FAMILY, 14, "bold"), **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.text = text
        self.command = command
        self.radius = radius
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = font
        self.config(bg=bg_color)

        self.bind("<Configure>", self._draw_button)
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>",
                  lambda e: self._draw_button(fill_color=BTN_ACTIVE if self.bg_color == BTN_COLOR else "#C0392B"))
        self.bind("<Leave>", lambda e: self._draw_button(fill_color=self.bg_color))
        self.config(cursor="hand2")

    def _draw_button(self, event=None, fill_color=None):
        """Draws the rounded button shape and text."""
        self.delete("all")
        w, h = int(self.winfo_width()), int(self.winfo_height())
        r = self.radius
        color = fill_color if fill_color else self.bg_color

        self.create_arc((0, h - 2 * r, 2 * r, h), start=180, extent=90, fill=color, outline="")
        self.create_arc((w - 2 * r, h - 2 * r, w, h), start=270, extent=90, fill=color, outline="")
        self.create_arc((0, 0, 2 * r, 2 * r), start=90, extent=90, fill=color, outline="")
        self.create_arc((w - 2 * r, 0, w, 2 * r), start=0, extent=90, fill=color, outline="")
        self.create_rectangle(r, 0, w - r, h, fill=color, outline="")
        self.create_rectangle(0, r, w, h - r, fill=color, outline="")

        self.create_text(w / 2, h / 2, text=self.text, font=self.font, fill=self.text_color, anchor="center")

    def _on_click(self, event):
        """Executes the command when the button is clicked."""
        if self.command and callable(self.command):
            self.command()


class RoundedCornerWindow(tk.Frame):
    """
    A custom Tkinter Frame that creates a window with rounded corners and a draggable header.
    It acts as the main container for Toplevel windows that use this style.
    """

    def __init__(self, master=None, radius=25, bg="#FFFDF6", **kwargs):
        super().__init__(master, bg=bg, **kwargs)
        self.master = master
        self.radius = radius
        self.bg = bg
        self.config(bd=0, highlightthickness=0)
        self.canvas = tk.Canvas(self, bg=self.master['bg'], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.bind("<Configure>", self._draw_rounded_rect)

        self.header_height = 60
        self._x = 0
        self._y = 0
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        """Records the starting position for dragging."""
        if 0 <= event.y < self.header_height:
            self._x = event.x
            self._y = event.y
        else:
            self._x = None
            self._y = None

    def do_move(self, event):
        """Moves the window based on mouse drag."""
        if self._x is not None and self._y is not None:
            deltax = event.x - self._x
            deltay = event.y - self._y
            x = self.master.winfo_x() + deltax
            y = self.master.winfo_y() + deltay
            self.master.geometry(f"+{x}+{y}")

    def _draw_rounded_rect(self, event):
        """Draws the rounded rectangle shape for the window frame."""
        self.canvas.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        r = self.radius
        header_height = self.header_height
        header_color = BTN_COLOR
        fill_color = self.bg

        self.canvas.create_arc((0, 0, 2 * r, 2 * r), start=90, extent=90, fill=fill_color, outline="")
        self.canvas.create_arc((w - 2 * r, 0, w, 2 * r), start=0, extent=90, fill=fill_color, outline="")
        self.canvas.create_arc((0, h - 2 * r, 2 * r, h), start=180, extent=90, fill=fill_color, outline="")
        self.canvas.create_arc((w - 2 * r, h - 2 * r, w, h), start=270, extent=90, fill=fill_color, outline="")
        self.canvas.create_rectangle(r, 0, w - r, h, fill=fill_color, outline="")
        self.canvas.create_rectangle(0, r, w, h - r, fill=fill_color, outline="")

        self.canvas.create_rectangle(0, 0, w, header_height - r, fill=header_color, outline="")
        self.canvas.create_rectangle(r, 0, w - r, header_height, fill=header_color, outline="")

        self.canvas.create_arc(0, header_height - 2 * r, 2 * r, header_height, start=180, extent=90, fill=header_color,
                               outline="")
        self.canvas.create_arc(w - 2 * r, header_height - 2 * r, w, header_height, start=270, extent=90,
                               fill=header_color, outline="")


if __name__ == "__main__":
    database_manager.initialize_db()
    root_app = tk.Tk()
    root_app.withdraw()

    # Directly open the SelectExpenseToEditWindow
    select_window = SelectExpenseToEditWindow(root_app)
    root_app.mainloop()